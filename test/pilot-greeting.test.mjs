import test from 'node:test';
import assert from 'node:assert/strict';
import { greeting } from '../pilot-greeting.mjs';

test('greets the default world and a supplied name', () => {
  assert.equal(greeting(), 'Hello, world!');
  assert.equal(greeting(undefined), 'Hello, world!');
  assert.equal(greeting('Ada'), 'Hello, Ada!');
});

test('preserves an empty name', () => {
  assert.equal(greeting(''), 'Hello, !');
});

test('rejects non-string names with TypeError', () => {
  for (const name of [null, 0, NaN, true, {}, [], Symbol('name'), 1n, () => {}]) {
    assert.throws(() => greeting(name), TypeError);
  }
});
