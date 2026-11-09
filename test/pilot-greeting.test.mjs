import test from 'node:test';
import assert from 'node:assert/strict';
import { greeting } from '../pilot-greeting.mjs';

test('greets the default world and supplied names', () => {
  assert.equal(greeting(), 'Hello, world!');
  assert.equal(greeting(undefined), 'Hello, world!');
  assert.equal(greeting('Ada'), 'Hello, Ada!');
});

test('preserves an empty string', () => {
  assert.equal(greeting(''), 'Hello, !');
});

test('rejects non-string arguments', () => {
  for (const value of [null, 0, NaN, true, {}, [], new String('Ada'), Symbol('Ada'), 1n]) {
    assert.throws(() => greeting(value), TypeError);
  }
});
