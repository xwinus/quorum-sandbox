"""Checks for the file-based greeting companion greet-file.sh."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'greet-file.sh'
DEFAULT = 'Hello from quorum-sandbox\n'


class GreetFileTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def write(self, data, name='names.txt'):
        path = self.tmp / name
        path.write_bytes(data)
        return path

    def run_script(self, *args):
        return subprocess.run(['sh', str(SCRIPT), *args], capture_output=True)

    def assert_greeting(self, data, expected):
        path = self.write(data)
        result = self.run_script(str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, expected.encode('utf-8'))
        self.assertEqual(result.stderr, b'')
        self.assertEqual(path.read_bytes(), data, 'input file must be unchanged')

    def assert_failure(self, result, status, stderr_fragment):
        self.assertEqual(result.returncode, status)
        self.assertEqual(result.stdout, b'')
        stderr = result.stderr.decode('utf-8')
        self.assertIn(stderr_fragment, stderr)
        self.assertEqual(stderr.count('\n'), 1, 'diagnostic should be one line')
        self.assertNotIn('Hello', stderr)

    # Normal cases

    def test_only_first_line_is_used(self):
        self.assert_greeting(b'Ada\nGrace\n', 'Hello, Ada, from quorum-sandbox\n')

    def test_single_line_without_trailing_newline(self):
        self.assert_greeting(b'Ada', 'Hello, Ada, from quorum-sandbox\n')

    def test_utf8_name(self):
        self.assert_greeting('Zoë Ångström\n'.encode('utf-8'),
                             'Hello, Zoë Ångström, from quorum-sandbox\n')

    # Edge cases

    def test_empty_file_uses_default(self):
        self.assert_greeting(b'', DEFAULT)

    def test_empty_first_line_uses_default(self):
        self.assert_greeting(b'\nGrace\n', DEFAULT)

    # Only LF separates lines; a carriage return is name data.

    def test_crlf_keeps_carriage_return_in_name(self):
        self.assert_greeting(b'Ada\r\nGrace\r\n', 'Hello, Ada\r, from quorum-sandbox\n')

    def test_lone_carriage_return_line_is_a_name(self):
        self.assert_greeting(b'\r\nGrace\r\n', 'Hello, \r, from quorum-sandbox\n')

    def test_carriage_return_at_end_of_file_is_kept(self):
        self.assert_greeting(b'Ada\r', 'Hello, Ada\r, from quorum-sandbox\n')

    def test_lone_carriage_return_at_end_of_file_is_a_name(self):
        self.assert_greeting(b'\r', 'Hello, \r, from quorum-sandbox\n')

    def test_format_characters_and_backslashes_are_literal(self):
        self.assert_greeting(b'Ada %s \\n\n', 'Hello, Ada %s \\n, from quorum-sandbox\n')

    def test_option_like_name_is_literal(self):
        self.assert_greeting(b'--help\n', 'Hello, --help, from quorum-sandbox\n')

    def test_surrounding_spaces_are_kept(self):
        self.assert_greeting(b'  Ada  \n', 'Hello,   Ada  , from quorum-sandbox\n')

    def test_option_like_file_name_is_a_path(self):
        path = self.write(b'Ada\n', name='-n')
        result = subprocess.run(['sh', str(SCRIPT), '-n'], capture_output=True, cwd=self.tmp)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b'Hello, Ada, from quorum-sandbox\n')
        self.assertEqual(path.read_bytes(), b'Ada\n')

    # Error cases

    def test_no_argument_is_a_usage_error(self):
        self.assert_failure(self.run_script(), 2, 'usage: greet-file.sh FILE')

    def test_too_many_arguments_is_a_usage_error(self):
        first = self.write(b'Ada\n', name='a.txt')
        second = self.write(b'Grace\n', name='b.txt')
        self.assert_failure(self.run_script(str(first), str(second)), 2,
                            'usage: greet-file.sh FILE')

    def test_missing_file_fails(self):
        missing = self.tmp / 'missing.txt'
        self.assert_failure(self.run_script(str(missing)), 1,
                            f'greet-file.sh: cannot read FILE: {missing}')

    def test_empty_path_fails(self):
        self.assert_failure(self.run_script(''), 1, 'greet-file.sh: cannot read FILE: ')

    def test_directory_fails(self):
        self.assert_failure(self.run_script(str(self.tmp)), 1,
                            f'greet-file.sh: cannot read FILE: {self.tmp}: is a directory')

    @unittest.skipIf(hasattr(os, 'geteuid') and os.geteuid() == 0,
                     'root can read files without read permission')
    def test_unreadable_file_fails(self):
        path = self.write(b'Ada\n')
        path.chmod(0o200)
        self.addCleanup(path.chmod, 0o600)
        self.assert_failure(self.run_script(str(path)), 1,
                            f'greet-file.sh: cannot read FILE: {path}')


if __name__ == '__main__':
    unittest.main()
