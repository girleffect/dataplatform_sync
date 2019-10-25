from unittest.mock import patch

from django.test import TestCase
from .. import tasks


def run(cmd, **kwargs):
    class Status:
        returncode = 0

    return Status()


class GCDataSync(TestCase):
    @patch('subprocess.run', run)
    def test_success_async(self):
        files = 'tests/*.csv'
        directory = 'tests'
        self.assertTrue(
            tasks.gc_data_sync(files=files, directory=directory))

    @patch('subprocess.run', run)
    def test_success(self):
        files = 'tests/*.csv'
        directory = 'tests'
        self.assertTrue(
            tasks.gc_data_sync(files=files, directory=directory))

    @patch('subprocess.run', run)
    def test_success_func_arg(self):
        kw = {
            'files': 'testfile{}.csv',
            'timestamped_files': True,
            'timestamped_format': '%Y%m%d',
            'directory': 'test',
        }
        self.assertTrue(tasks.gc_data_sync(**kw))

    def test_invalid_args(self):
        try:
            self.assertTrue(tasks.gc_data_sync())
        except tasks.ShellExecutionException:
            pass
        self.assertRaises(tasks.ShellExecutionException)

    def test_invalid_args_async(self):
        self.assertTrue(tasks.gc_data_sync)
        self.assertRaises(tasks.ShellExecutionException)

    @patch('ge_sm.control.main')
    @patch('subprocess.run', run)
    def test_run_ge_sm(self, p1):
        self.assertTrue(tasks.run_ge_sm('2019-06-01', '2019-08-01'))
        p1.assert_called_once()
        p1.assert_called_with('2019-06-01', '2019-08-01')
