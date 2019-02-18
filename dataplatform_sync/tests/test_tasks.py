from unittest.mock import patch

from django.test import TestCase
from .. import tasks


def run(cmd, **kwargs):
    class Status:
        returncode = 0

    return Status()


class GCDataSync(TestCase):

    def test_success_async(self):
        files = 'tests/*.csv'
        directory = 'tests'
        self.assertTrue(
            tasks.gc_data_sync.delay(files=files, directory=directory))

    @patch('subprocess.run', run)
    def test_success(self):
        files = 'tests/*.csv'
        directory = 'tests'
        self.assertTrue(
            tasks.gc_data_sync(files=files, directory=directory))

    def test_success_func_arg(self):
        def file_name():
            return 'tests/*.csv'

        def dir_name():
            return 'tests'

        self.assertTrue(tasks.gc_data_sync(
            files=file_name, directory=dir_name))

    def test_invalid_args(self):
        try:
            self.assertTrue(tasks.gc_data_sync())
        except tasks.ShellExecutionException:
            pass
        self.assertRaises(tasks.ShellExecutionException)

    def test_invalid_args_async(self):
        self.assertTrue(tasks.gc_data_sync.delay())
        self.assertRaises(tasks.ShellExecutionException)
