from unittest.mock import patch
from django.test import TestCase
from .. import tasks


def run(cmd, **kwargs):

    class Status:
        returncode = 0

    return Status()


class GCDataSync(TestCase):
    @patch('subprocess.run', run)
    def test_success(self):
        files = 'tests/*.csv'
        directory = 'tests'
        self.assertTrue(
            tasks.gc_data_sync.delay(files=files, directory=directory))

    def test_invalid_args(self):
        try:
            self.assertTrue(tasks.gc_data_sync.delay())
        except tasks.ShellExecutionException:
            pass
        self.assertRaises(tasks.ShellExecutionException)
