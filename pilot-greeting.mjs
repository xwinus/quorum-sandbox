export function greeting(name = 'world') {
  if (typeof name !== 'string') {
    throw new TypeError('Name must be a string');
  }

  return 'Hello, ' + name + '!';
}
