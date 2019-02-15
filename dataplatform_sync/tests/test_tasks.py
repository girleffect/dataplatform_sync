from django.test import TestCase
from .. import tasks


class GCDataSync(TestCase):

    def test_success_async(self):
        files = 'tests/*.csv'
        directory = 'tests'
        self.assertTrue(
            tasks.gc_data_sync.delay(files=files, directory=directory))

    def test_success(self):
        files = 'tests/*.csv'
        directory = 'tests'
        self.assertTrue(
            tasks.gc_data_sync(files=files, directory=directory))

    def test_invalid_args(self):
        try:
            self.assertTrue(tasks.gc_data_sync())
        except tasks.ShellExecutionException:
            pass
        self.assertRaises(tasks.ShellExecutionException)

    def test_invalid_args_async(self):
        self.assertTrue(tasks.gc_data_sync.delay())
        self.assertRaises(tasks.ShellExecutionException)
