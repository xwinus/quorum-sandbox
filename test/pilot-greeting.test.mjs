import test from 'node:test';
import assert from 'node:assert/strict';
import { greeting } from '../pilot-greeting.mjs';

test('greets the default world and a supplied name', () => {
  assert.equal(greeting(), 'Hello, world!');
  assert.equal(greeting(undefined), 'Hello, world!');
  assert.equal(greeting('Ada'), 'Hello, Ada!');
});

test('preserves an empty string', () => {
  assert.equal(greeting(''), 'Hello, !');
});

test('rejects non-string arguments with TypeError', () => {
  for (const value of [null, 0, true, {}, [], Symbol('name'), 1n, () => 'Ada']) {
    assert.throws(() => greeting(value), TypeError);
  }
});
