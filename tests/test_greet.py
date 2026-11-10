"""Regression checks for the positional greeting and --repeat interfaces."""
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'greet.sh'
USAGE = 'Usage: greet.sh --repeat {1|2|3} [NAME]\n'
DEFAULT = 'Hello from quorum-sandbox\n'


def run_greet(args):
    return subprocess.run(['sh', str(SCRIPT), *args], capture_output=True, text=True)


class GreetingTests(unittest.TestCase):
    def assert_greeting(self, args, expected):
        result = run_greet(args)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, '')

    def test_no_arguments_uses_default(self):
        self.assert_greeting([], DEFAULT)

    def test_named_greeting(self):
        self.assert_greeting(['Ada'], 'Hello, Ada, from quorum-sandbox\n')

    def test_option_like_name_is_literal(self):
        self.assert_greeting(['--help'], 'Hello, --help, from quorum-sandbox\n')

    def test_empty_name_uses_default(self):
        self.assert_greeting([''], DEFAULT)

    def test_format_characters_are_literal(self):
        self.assert_greeting(['Ada %s'], 'Hello, Ada %s, from quorum-sandbox\n')

    def test_subsequent_arguments_are_ignored(self):
        self.assert_greeting(['Ada', 'Grace'], 'Hello, Ada, from quorum-sandbox\n')

    def test_empty_first_argument_ignores_subsequent_arguments(self):
        self.assert_greeting(['', 'Grace'], DEFAULT)

    def test_repeat_after_a_name_is_ignored(self):
        self.assert_greeting(['Ada', '--repeat', '2'], 'Hello, Ada, from quorum-sandbox\n')

    def test_repeat_with_equals_sign_is_a_literal_name(self):
        self.assert_greeting(['--repeat=2'], 'Hello, --repeat=2, from quorum-sandbox\n')


class RepeatTests(unittest.TestCase):
    def assert_greeting(self, args, expected):
        result = run_greet(args)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, '')

    def test_each_count_prints_the_default_greeting_that_many_times(self):
        for count in (1, 2, 3):
            with self.subTest(count=count):
                self.assert_greeting(['--repeat', str(count)], DEFAULT * count)

    def test_each_count_prints_the_named_greeting_that_many_times(self):
        for count in (1, 2, 3):
            with self.subTest(count=count):
                self.assert_greeting(
                    ['--repeat', str(count), 'Ada'],
                    'Hello, Ada, from quorum-sandbox\n' * count,
                )

    def test_empty_name_uses_default(self):
        self.assert_greeting(['--repeat', '2', ''], DEFAULT * 2)

    def test_names_are_preserved_literally(self):
        names = (
            'Ada %s',
            'Ada %d%%',
            'Ada\\nLovelace',
            'Ada  Lovelace',
            ' Ada ',
            'Ada\nLovelace',
            '$HOME',
            '$(echo x)',
            '`echo x`',
            '*',
            '-n',
            '--',
            '--help',
            '--repeat',
            '1',
        )
        for name in names:
            with self.subTest(name=name):
                self.assert_greeting(
                    ['--repeat', '2', name],
                    f'Hello, {name}, from quorum-sandbox\n' * 2,
                )


class RepeatErrorTests(unittest.TestCase):
    def assert_usage_error(self, args):
        result = run_greet(args)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, USAGE)

    def test_missing_count(self):
        self.assert_usage_error(['--repeat'])

    def test_invalid_counts(self):
        counts = (
            '',
            '0',
            '4',
            '-1',
            'abc',
            '01',
            '001',
            '+1',
            ' 1',
            '1 ',
            '1\n',
            '1.0',
            '1e0',
            '0x1',
            '10',
            '1|2',
            '*',
            '?',
            '--repeat',
        )
        for count in counts:
            with self.subTest(count=count):
                self.assert_usage_error(['--repeat', count])

    def test_invalid_count_with_a_name(self):
        self.assert_usage_error(['--repeat', '4', 'Ada'])

    def test_name_in_place_of_the_count(self):
        self.assert_usage_error(['--repeat', 'Ada'])

    def test_more_than_one_name(self):
        extras = (
            ['Ada', 'Grace'],
            ['Ada', 'Grace', 'Edsger'],
            ['', 'Grace'],
            ['Ada', ''],
            ['', ''],
        )
        for names in extras:
            with self.subTest(names=names):
                self.assert_usage_error(['--repeat', '2', *names])


if __name__ == '__main__':
    unittest.main()
