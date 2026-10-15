# gr2_unbitknit

Rewrites Granny 2.11 `.gr2` files (format 7) whose sections are BitKnit2-compressed so that the sections and their relocation tables are stored raw. The port's reader handles only raw and Oodle1 sections.

- `bitknit.c`: BitKnit decoder from [libbg3](https://github.com/eiz/libbg3) `examples/bitknit.c`, itself adapted from [ooz](https://github.com/powzix/ooz) (GPL-3.0, see the file header). Used only at build time; nothing of it is linked into the client.
- `gr2_unbitknit.c`: the converter.

```sh
gcc -O2 -o gr2_unbitknit gr2_unbitknit.c
./gr2_unbitknit /work/kit/build/port/client_files /work/kit/build/port/repaired_gr2
```

`build_corpus.py` overlays `repaired_gr2/` onto the corpus under the same names. Run it after `unpack` and before `corpus`.
