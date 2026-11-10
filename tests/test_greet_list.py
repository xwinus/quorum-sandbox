"""Checks for the line-by-line greeting companion greet-list.sh."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'greet-list.sh'
DEFAULT = 'Hello from quorum-sandbox\n'


def hello(name):
    return f'Hello, {name}, from quorum-sandbox\n'


class GreetListTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def write(self, data, name='names.txt'):
        path = self.tmp / name
        path.write_bytes(data)
        return path

    def run_script(self, *args, cwd=None):
        return subprocess.run(['sh', str(SCRIPT), *args], capture_output=True, cwd=cwd)

    def assert_greetings(self, data, expected):
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

    def test_each_line_is_greeted(self):
        self.assert_greetings(b'Ada\nGrace\n', hello('Ada') + hello('Grace'))

    def test_utf8_names(self):
        self.assert_greetings('Zoë\nÅngström\n'.encode('utf-8'),
                              hello('Zoë') + hello('Ångström'))

    # Line endings

    def test_final_line_without_newline_is_greeted_once(self):
        self.assert_greetings(b'Ada\nGrace', hello('Ada') + hello('Grace'))

    def test_single_line_without_newline_is_greeted_once(self):
        self.assert_greetings(b'Ada', hello('Ada'))

    def test_trailing_newline_adds_no_phantom_name(self):
        self.assert_greetings(b'Ada\n', hello('Ada'))

    # Empty lines and files

    def test_empty_file_prints_nothing(self):
        self.assert_greetings(b'', '')

    def test_single_empty_line_uses_default(self):
        self.assert_greetings(b'\n', DEFAULT)

    def test_every_empty_line_uses_default(self):
        self.assert_greetings(b'\nAda\n\n\nGrace\n\n',
                              DEFAULT + hello('Ada') + DEFAULT + DEFAULT + hello('Grace') + DEFAULT)

    # Names are literal

    def test_surrounding_spaces_are_kept(self):
        self.assert_greetings(b'  Ada  \n \n', hello('  Ada  ') + hello(' '))

    def test_tabs_are_kept(self):
        self.assert_greetings(b'\tAda\t\n', hello('\tAda\t'))

    def test_backslashes_are_literal(self):
        self.assert_greetings(b'Ada \\n\nC:\\temp\\\n', hello('Ada \\n') + hello('C:\\temp\\'))

    def test_trailing_backslash_does_not_join_lines(self):
        self.assert_greetings(b'Ada\\\nGrace\n', hello('Ada\\') + hello('Grace'))

    def test_percent_characters_are_literal(self):
        self.assert_greetings(b'100%\n%s %d %%\n', hello('100%') + hello('%s %d %%'))

    def test_option_like_names_are_literal(self):
        self.assert_greetings(b'--help\n-n\n-e\n--\n',
                              hello('--help') + hello('-n') + hello('-e') + hello('--'))

    def test_glob_characters_are_literal(self):
        self.assert_greetings(b'*\n?\n', hello('*') + hello('?'))

    # Only LF separates lines; a carriage return is name data.

    def test_crlf_keeps_carriage_return_in_names(self):
        self.assert_greetings(b'Ada\r\nGrace\r\n', hello('Ada\r') + hello('Grace\r'))

    def test_lone_carriage_return_line_is_a_name(self):
        self.assert_greetings(b'\r\n\n', hello('\r') + DEFAULT)

    def test_carriage_return_at_end_of_file_is_kept(self):
        self.assert_greetings(b'Ada\nGrace\r', hello('Ada') + hello('Grace\r'))

    def test_lone_carriage_return_at_end_of_file_is_a_name(self):
        self.assert_greetings(b'\r', hello('\r'))

    # Paths

    def test_option_like_file_name_is_a_path(self):
        path = self.write(b'Ada\nGrace\n', name='-n')
        result = self.run_script('-n', cwd=self.tmp)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (hello('Ada') + hello('Grace')).encode('utf-8'))
        self.assertEqual(path.read_bytes(), b'Ada\nGrace\n')

    # Error cases

    def test_no_argument_is_a_usage_error(self):
        self.assert_failure(self.run_script(), 2, 'usage: greet-list.sh FILE')

    def test_too_many_arguments_is_a_usage_error(self):
        first = self.write(b'Ada\n', name='a.txt')
        second = self.write(b'Grace\n', name='b.txt')
        self.assert_failure(self.run_script(str(first), str(second)), 2,
                            'usage: greet-list.sh FILE')
        self.assertEqual(first.read_bytes(), b'Ada\n')
        self.assertEqual(second.read_bytes(), b'Grace\n')

    def test_missing_file_fails(self):
        missing = self.tmp / 'missing.txt'
        self.assert_failure(self.run_script(str(missing)), 1,
                            f'greet-list.sh: cannot read FILE: {missing}')
        self.assertFalse(missing.exists())

    def test_empty_path_fails(self):
        self.assert_failure(self.run_script(''), 1, 'greet-list.sh: cannot read FILE: ')

    def test_directory_fails(self):
        self.assert_failure(self.run_script(str(self.tmp)), 1,
                            f'greet-list.sh: cannot read FILE: {self.tmp}: is a directory')

    @unittest.skipIf(hasattr(os, 'geteuid') and os.geteuid() == 0,
                     'root can read files without read permission')
    def test_unreadable_file_fails(self):
        path = self.write(b'Ada\nGrace\n')
        path.chmod(0o200)
        self.addCleanup(path.chmod, 0o600)
        self.assert_failure(self.run_script(str(path)), 1,
                            f'greet-list.sh: cannot read FILE: {path}')
        path.chmod(0o600)
        self.assertEqual(path.read_bytes(), b'Ada\nGrace\n')


if __name__ == '__main__':
    unittest.main()
