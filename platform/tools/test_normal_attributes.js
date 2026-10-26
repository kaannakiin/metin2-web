// Read-only regression checks for the 2026-10-22 attribute data migration.
// Run: node --test platform/tools/test_normal_attributes.js
const assert = require('node:assert/strict');
const { createHash } = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');

const root = path.resolve(__dirname, '../..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const seed = read('content/server/sql/seed_item_attr.sql');
const migration = read('content/server/sql/migrations/20261022_normal_attributes.sql');
const tuples = text => [...text.matchAll(/\('([^']+)',\s*([\d,\s]+)\)/g)]
  .map(m => [m[1], m[2].split(',').map(Number)]);
const [normalText, rareText] = seed.split('INSERT INTO `item_attr_rare`');
const normal = tuples(normalText);
const rare = tuples(rareText);
const changes = tuples(migration);
const byId = new Map(normal);
const fixedIds = new Set(changes.map(([id]) => id));
const sets = ['weapon', 'body', 'wrist', 'foots', 'neck', 'head', 'shield', 'ear'];
const allowed = id => sets.filter((_, index) => byId.get(id)[6 + index] > 0);
const hash = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');

test('seed and targeted migration have complete, unique, valid rows', () => {
  assert.equal(normal.length, 59);
  assert.equal(byId.size, 59);
  assert.equal(rare.length, 39);
  assert.equal(changes.length, 45);
  assert.equal(fixedIds.size, 45);
  for (const [id, values] of normal) {
    assert.equal(values.length, 18, id);
    assert.ok(values[0] > 0, id);
    assert.ok(values.slice(6).every(v => Number.isInteger(v) && v >= 0 && v <= 5), id);
  }
  for (const [id, values] of changes) {
    assert.equal(values.length, 9, id);
    assert.ok(byId.has(id), id);
    assert.deepEqual(byId.get(id).slice(1, 6), Array(5).fill(values[0]), id);
    assert.deepEqual(byId.get(id).slice(6, 14), values.slice(1), id);
  }
});

test('every possible generated level returns the fixed value in every enabled set', () => {
  for (const [id, [fixedValue]] of changes) {
    const values = byId.get(id);
    for (const cap of values.slice(6).filter(Boolean)) {
      // Matches PutAttributeWithLevel + AddAttr; also covers costume/pendant
      // caps and both add/reroll distributions without a random/flaky test.
      for (let level = 1; level <= 5; level++) {
        assert.equal(values[Math.min(level, cap)], fixedValue, `${id}, level ${level}, cap ${cap}`);
      }
    }
  }
});

test('HP 3000 is restricted to the four classic standard equipment sets', () => {
  assert.deepEqual(byId.get('MAX_HP').slice(1, 6), [3000, 3000, 3000, 3000, 3000]);
  assert.deepEqual(allowed('MAX_HP'), ['body', 'wrist', 'foots', 'neck']);
  for (const id of ['CON', 'INT', 'STR', 'DEX']) {
    assert.deepEqual(allowed(id), ['weapon', 'shield']);
    assert.equal(byId.get(id)[1], 12);
  }
});

test('status effects and shield immunity have the corrected equipment permissions', () => {
  assert.deepEqual(allowed('POISON_PCT'), ['weapon', 'head']);
  assert.deepEqual(allowed('STUN_PCT'), ['weapon', 'foots', 'neck']);
  assert.deepEqual(allowed('SLOW_PCT'), ['weapon', 'foots']);
  for (const id of ['IMMUNE_STUN', 'IMMUNE_SLOW']) {
    assert.deepEqual(allowed(id), ['shield']);
    assert.equal(byId.get(id)[1], 1);
  }
});

test('damage, defense, speed and absorb bonuses do not leak into other standard sets', () => {
  const expected = {
    ATT_SPEED: ['foots', 'head'], MOV_SPEED: ['ear'], CAST_SPEED: ['weapon', 'body'],
    CRITICAL_PCT: ['weapon', 'foots', 'neck'], PENETRATE_PCT: ['weapon', 'wrist', 'neck'],
    STEAL_HP: ['body', 'wrist'], STEAL_SP: ['body', 'neck', 'head'],
    MANA_BURN_PCT: ['wrist', 'neck', 'ear'], ATT_GRADE_BONUS: ['body'],
    BLOCK: ['shield'], DODGE: ['foots', 'head'], REFLECT_MELEE: ['body', 'shield'],
  };
  for (const [id, slots] of Object.entries(expected)) assert.deepEqual(allowed(id), slots, id);
  for (const suffix of ['SWORD', 'TWOHAND', 'DAGGER', 'BELL', 'FAN', 'BOW']) {
    assert.deepEqual(allowed(`RESIST_${suffix}`), ['body', 'foots', 'neck', 'ear']);
    assert.equal(byId.get(`RESIST_${suffix}`)[1], 15);
  }
  for (const suffix of ['FIRE', 'ELEC', 'MAGIC', 'WIND']) {
    assert.deepEqual(allowed(`RESIST_${suffix}`), ['body', 'wrist', 'head']);
  }
});

test('14 non-classic bonuses cannot roll in any normal or costume set', () => {
  const deferred = normal.filter(([id]) => !fixedIds.has(id));
  assert.equal(deferred.length, 14);
  assert.ok(deferred.every(([, values]) => values.slice(6).every(value => value === 0)));
  assert.equal(hash(deferred.map(([id, v]) => [id, v.slice(0, 6)])),
    '8020ca618cb934fddcfc4a6cbd30f8bc3017b1e7d6361c5917a0c3be7478c921');
});

test('rare pool, weights and pendant/costume permissions preserve their prior values', () => {
  assert.equal(hash(rare), 'dc4e4b939ed895bfede4e152ccbb6c07e6459c502b3b997782e47c7f3b71eb94');
  assert.equal(hash(normal.map(([id, v]) => [id, v[0], ...(fixedIds.has(id) ? v.slice(14) : [])])),
    '19347eac81eb64a7cfcd53b7b468c60c6d73603481f8fc64559806bfad401db1');
});

test('classic permissions migration updates only the 14 blocked rows and all 12 masks', () => {
  const sql = read('content/server/sql/migrations/20261022_classic_attribute_permissions.sql')
    .replace(/^--.*$/gm, '');
  const ids = [...sql.matchAll(/\('([A-Z_]+)'\)/g)].map(m => m[1]);
  assert.deepEqual(new Set(ids), new Set(normal.filter(([id]) => !fixedIds.has(id)).map(([id]) => id)));
  assert.equal(ids.length, 14);
  const fields = [...sql.matchAll(/a\.(\w+)=0/g)].map(m => m[1]);
  assert.deepEqual(fields, [...sets, 'pendant', 'costume_body', 'costume_hair', 'costume_weapon']);
  assert.match(sql, /COUNT\(\*\) = 14 AND COUNT\(DISTINCT a\.`apply`\) = 14/);
  assert.doesNotMatch(sql, /\b(?:DELETE|TRUNCATE|REPLACE|ALTER)\b/i);
  assert.doesNotMatch(sql, /\bitem_attr_rare\b|\bplayer\.item\b/);
});

test('migration changes only targeted fields and never rewrites player equipment or rare pool', () => {
  const sql = migration.replace(/^--.*$/gm, '');
  const update = sql.match(/UPDATE item_attr AS a\s+JOIN normal_attribute_patch_20261022 AS p ON a\.`apply` = p\.`apply`\s+SET ([\s\S]*?);/);
  assert.ok(update, 'UPDATE must be restricted to the 45-row temporary patch');
  const assignments = [...update[1].matchAll(/a\.(\w+)\s*=/g)].map(m => m[1]);
  assert.deepEqual(assignments, ['lv1', 'lv2', 'lv3', 'lv4', 'lv5', ...sets]);
  assert.equal((sql.match(/\bUPDATE\b/g) || []).length, 1);
  assert.doesNotMatch(sql, /\b(?:DELETE|TRUNCATE|REPLACE|ALTER)\b/i);
  assert.doesNotMatch(sql, /\bitem_attr_rare\b|\bplayer\.item\b/);
  assert.match(sql, /CHECK \(`valid` = 1\)/);
  assert.match(sql, /COUNT\(\*\) = 45 AND COUNT\(DISTINCT a\.`apply`\) = 45/);
  assert.ok(sql.indexOf('normal_attribute_guard_20261022\nSELECT') < sql.indexOf('UPDATE item_attr'));
  assert.match(sql, /START TRANSACTION;[\s\S]*UPDATE item_attr[\s\S]*COMMIT;/);
});
