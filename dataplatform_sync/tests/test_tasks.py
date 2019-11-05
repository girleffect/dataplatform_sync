import datetime
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
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
        fmt = "%Y-%m-%d"
        today = datetime.datetime.now()
        tm = datetime.datetime.strftime(
            today + datetime.timedelta(days=2), fmt)
        month0 = datetime.datetime.strftime(
            today.replace(day=1), fmt)
        month1 = datetime.datetime.strftime(
            today - datetime.timedelta(days=90), fmt)

        self.assertTrue(tasks.run_ge_sm())
        p1.assert_called_once()
        p1.assert_called_with(month0, month1, tm)


class TestViews(TestCase):

    def test_tasks_view(self):
        res = self.client.get(reverse('tasks'))
        self.assertEqual(res.status_code, 200)
        self.assertTrue('form' in res.context_data.keys())
        self.assertTrue('task' in res.context_data['form'].fields.keys())
        self.assertTrue('delay' in res.context_data['form'].fields.keys())
        # self.assertTrue('args' in res.context_data['form'].fields.keys())
        # self.assertTrue('kwargs' in res.context_data['form'].fields.keys())

    @patch('ge_sm.control.main')
    @patch('subprocess.run', run)
    def test_tasks_view_post(self, p1):
        data = {'task': 'dataplatform_sync.tasks.run_ge_sm', 'delay': ''}
        res = self.client.post(reverse('tasks'), data=data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('tasks'))

        fmt = "%Y-%m-%d"
        today = datetime.datetime.now()
        tm = datetime.datetime.strftime(
            today + datetime.timedelta(days=2), fmt)
        month0 = datetime.datetime.strftime(
            today.replace(day=1), fmt)
        month1 = datetime.datetime.strftime(
            today - datetime.timedelta(days=90), fmt)

        p1.assert_called_once()
        p1.assert_called_with(month0, month1, tm)

    def test_tasks_view_post_invalid(self):
        res = self.client.post(reverse('tasks'), data={})
        self.assertEqual(res.status_code, 200)
        self.assertTrue('form' in res.context_data.keys())
        self.assertTrue('task' in res.context_data['form'].errors.keys())
        self.assertEqual(
            res.context_data['form'].errors['task'],
            ['This field is required.']
        )
