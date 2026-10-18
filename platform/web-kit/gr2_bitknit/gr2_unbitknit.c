// gr2_unbitknit - rewrites Granny 2.11 (.gr2 format 7) files whose sections
// are BitKnit2-compressed into the same file with those sections and their
// relocation tables stored raw, so the port's reader (Oodle1 and raw only)
// can load them. Sections in other encodings are copied unchanged.
//
// Usage: gr2_unbitknit <source root> <target root>
//   every *.gr2 under the source root with a BitKnit2 section is written to
//   the same relative path under the target root; others are skipped.
//
// The BitKnit2 decoder (bitknit.c) and the quantum loop follow libbg3
// (github.com/eiz/libbg3, examples/granny.c and examples/bitknit.c).

#define _XOPEN_SOURCE 700
#include <errno.h>
#include <ftw.h>
#include <stdbool.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/stat.h>

#include "bitknit.c"

enum { kSectionEntry = 44, kRelocation = 12, kMarshal = 16, kBitknit2 = 4 };
#define BITKNIT2_MAGIC 0x75B1

static const char* g_source_root;
static const char* g_target_root;
static int g_converted, g_failed, g_scanned;

static uint32_t rd32(const uint8_t* p) {
  uint32_t v;
  memcpy(&v, p, 4);
  return v;
}

static void wr32(uint8_t* p, uint32_t v) {
  memcpy(p, &v, 4);
}

// One BitKnit2 stream (magic, then 64 KiB quanta) into dst[0..dst_len).
static bool bitknit2_decode(const uint8_t* src, size_t src_len, uint8_t* dst, size_t dst_len) {
  if (!dst_len)
    return true;
  if (src_len < 2 || (src[0] | (src[1] << 8)) != BITKNIT2_MAGIC)
    return false;
  BitknitState* state = malloc(sizeof(BitknitState));
  if (!state)
    return false;
  BitknitState_Init(state);
  const uint8_t* src_cur = src + 2;
  const uint8_t* src_end = src + src_len;
  uint8_t* dst_cur = dst;
  uint8_t* dst_end = dst + dst_len;
  size_t quantum = 1;
  bool ok = true;
  while (dst_cur < dst_end) {
    size_t quantum_end = quantum * 65536 < dst_len ? quantum * 65536 : dst_len;
    if (src_end - src_cur < 2) {
      ok = false;
      break;
    }
    if (!(src_cur[0] | src_cur[1])) {
      src_cur += 2;
      size_t room = quantum_end - (size_t)(dst_cur - dst);
      size_t avail = (size_t)(src_end - src_cur);
      size_t n = room < avail ? room : avail;
      memcpy(dst_cur, src_cur, n);
      src_cur += n;
      dst_cur += n;
    } else {
      size_t used = Bitknit_Decode(src_cur, src_end, &dst_cur, dst + quantum_end, dst_end, dst, state);
      if (!used) {
        ok = false;
        break;
      }
      src_cur += used;
    }
    ++quantum;
  }
  free(state);
  return ok;
}

// A compressed fixup table: u32 compressed length, then a BitKnit2 stream.
static uint8_t* unpack_table(const uint8_t* file, size_t size, uint32_t offset, size_t out_len) {
  uint8_t* out = calloc(1, out_len ? out_len : 1);
  if (!out)
    return NULL;
  if (!out_len)
    return out;
  if ((uint64_t)offset + 4 > size)
    goto fail;
  uint32_t packed = rd32(file + offset);
  if ((uint64_t)offset + 4 + packed > size)
    goto fail;
  if (!bitknit2_decode(file + offset + 4, packed, out, out_len))
    goto fail;
  return out;
fail:
  free(out);
  return NULL;
}

typedef struct Blob {
  uint8_t* data;
  size_t len;
  bool owned;
} Blob;

static int make_parents(char* path) {
  for (char* p = path + 1; *p; ++p) {
    if (*p != '/')
      continue;
    *p = 0;
    if (mkdir(path, 0755) != 0 && errno != EEXIST) {
      *p = '/';
      return -1;
    }
    *p = '/';
  }
  return 0;
}

static void append(uint8_t** out, size_t* len, size_t* cap, const void* data, size_t n, size_t align) {
  size_t start = (*len + align - 1) / align * align;
  if (start + n > *cap) {
    *cap = (start + n) * 2;
    *out = realloc(*out, *cap);
  }
  memset(*out + *len, 0, start - *len);
  if (n)
    memcpy(*out + start, data, n);
  *len = start + n;
}

// Returns 1 converted, 0 nothing to do, -1 failure.
static int convert(const uint8_t* file, size_t size, uint8_t** result, size_t* result_len) {
  if (size < 32 + 20)
    return 0;
  const uint32_t base = 32;
  uint32_t section_table = rd32(file + base + 12);
  uint32_t sections = rd32(file + base + 16);
  if (!sections || sections > 64 || (uint64_t)base + section_table + (uint64_t)sections * kSectionEntry > size)
    return 0;
  const uint8_t* table = file + base + section_table;
  bool any = false;
  for (uint32_t i = 0; i < sections; ++i)
    if (rd32(table + i * kSectionEntry) == kBitknit2 && rd32(table + i * kSectionEntry + 12))
      any = true;
  if (!any)
    return 0;

  size_t header_len = base + section_table + (size_t)sections * kSectionEntry;
  uint8_t* out = NULL;
  size_t len = 0, cap = 0;
  append(&out, &len, &cap, file, header_len, 1);

  int status = 1;
  for (uint32_t i = 0; i < sections && status > 0; ++i) {
    const uint8_t* e = file + base + section_table + (size_t)i * kSectionEntry;
    uint32_t compression = rd32(e + 0), offset = rd32(e + 4), packed = rd32(e + 8),
             unpacked = rd32(e + 12), alignment = rd32(e + 16);
    uint32_t fix_off = rd32(e + 28), fixups = rd32(e + 32);
    uint32_t mar_off = rd32(e + 36), marshals = rd32(e + 40);
    size_t align = alignment >= 4 && alignment <= 4096 ? alignment : 4;
    Blob data = {0}, fix = {0}, mar = {0};

    if (compression == kBitknit2) {
      data.len = unpacked;
      data.data = calloc(1, unpacked ? unpacked : 1);
      data.owned = true;
      if (!data.data || (uint64_t)offset + packed > size ||
          !bitknit2_decode(file + offset, packed, data.data, unpacked))
        status = -1;
      fix.len = (size_t)fixups * kRelocation;
      fix.data = status > 0 ? unpack_table(file, size, fix_off, fix.len) : NULL;
      fix.owned = true;
      if (status > 0 && !fix.data)
        status = -1;
      mar.len = (size_t)marshals * kMarshal;
      mar.data = status > 0 ? unpack_table(file, size, mar_off, mar.len) : NULL;
      mar.owned = true;
      if (status > 0 && !mar.data)
        status = -1;
    } else {
      data.data = (uint8_t*)file + offset;
      data.len = packed;
      fix.data = (uint8_t*)file + fix_off;
      fix.len = (size_t)fixups * kRelocation;
      mar.data = (uint8_t*)file + mar_off;
      mar.len = (size_t)marshals * kMarshal;
      if ((uint64_t)offset + packed > size || (uint64_t)fix_off + fix.len > size ||
          (uint64_t)mar_off + mar.len > size)
        status = -1;
    }

    if (status > 0) {
      uint8_t* entry = out + base + section_table + (size_t)i * kSectionEntry;
      append(&out, &len, &cap, data.data, data.len, align);
      entry = out + base + section_table + (size_t)i * kSectionEntry;
      wr32(entry + 4, (uint32_t)(len - data.len));
      if (compression == kBitknit2) {
        wr32(entry + 0, 0);
        wr32(entry + 8, (uint32_t)data.len);
        wr32(entry + 20, (uint32_t)data.len);
        wr32(entry + 24, (uint32_t)data.len);
      }
      append(&out, &len, &cap, fix.data, fix.len, 4);
      entry = out + base + section_table + (size_t)i * kSectionEntry;
      wr32(entry + 28, (uint32_t)(len - fix.len));
      append(&out, &len, &cap, mar.data, mar.len, 4);
      entry = out + base + section_table + (size_t)i * kSectionEntry;
      wr32(entry + 36, (uint32_t)(len - mar.len));
    }
    if (data.owned)
      free(data.data);
    if (fix.owned)
      free(fix.data);
    if (mar.owned)
      free(mar.data);
  }
  if (status < 0) {
    free(out);
    return -1;
  }
  wr32(out + base + 4, (uint32_t)len);
  *result = out;
  *result_len = len;
  return 1;
}

static int visit(const char* path, const struct stat* st, int flag, struct FTW* ftw) {
  (void)ftw;
  size_t n = strlen(path);
  if (flag != FTW_F || n < 4 || strcasecmp(path + n - 4, ".gr2") != 0)
    return 0;
  ++g_scanned;
  FILE* f = fopen(path, "rb");
  if (!f)
    return 0;
  uint8_t* file = malloc(st->st_size ? st->st_size : 1);
  size_t got = file ? fread(file, 1, st->st_size, f) : 0;
  fclose(f);
  if (!file || got != (size_t)st->st_size) {
    free(file);
    return 0;
  }
  uint8_t* out = NULL;
  size_t out_len = 0;
  int r = convert(file, got, &out, &out_len);
  free(file);
  if (r < 0) {
    ++g_failed;
    fprintf(stderr, "FAILED %s\n", path);
    return 0;
  }
  if (r == 0)
    return 0;
  char target[4096];
  snprintf(target, sizeof(target), "%s/%s", g_target_root, path + strlen(g_source_root) + 1);
  FILE* o = NULL;
  if (make_parents(target) == 0)
    o = fopen(target, "wb");
  if (!o || fwrite(out, 1, out_len, o) != out_len) {
    ++g_failed;
    fprintf(stderr, "cannot write %s\n", target);
  } else {
    ++g_converted;
  }
  if (o)
    fclose(o);
  free(out);
  return 0;
}

int main(int argc, char** argv) {
  if (argc != 3) {
    fprintf(stderr, "usage: %s <source root> <target root>\n", argv[0]);
    return 2;
  }
  g_source_root = argv[1];
  g_target_root = argv[2];
  if (nftw(g_source_root, visit, 32, FTW_PHYS) != 0) {
    perror("nftw");
    return 1;
  }
  printf("gr2 files: %d | BitKnit2 unpacked: %d | failed: %d\n", g_scanned, g_converted, g_failed);
  return g_failed ? 1 : 0;
}
