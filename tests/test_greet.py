"""Regression checks for the existing positional greeting interface."""
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'greet.sh'


class GreetingTests(unittest.TestCase):
    def assert_greeting(self, args, expected):
        result = subprocess.run(['sh', str(SCRIPT), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, '')

    def test_named_greeting(self):
        self.assert_greeting(['Ada'], 'Hello, Ada, from quorum-sandbox\n')

    def test_option_like_name_is_literal(self):
        self.assert_greeting(['--help'], 'Hello, --help, from quorum-sandbox\n')

    def test_empty_name_uses_default(self):
        self.assert_greeting([''], 'Hello from quorum-sandbox\n')

    def test_format_characters_are_literal(self):
        self.assert_greeting(['Ada %s'], 'Hello, Ada %s, from quorum-sandbox\n')


if __name__ == '__main__':
    unittest.main()
