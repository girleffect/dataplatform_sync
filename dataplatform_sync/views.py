import importlib
from celery import current_app

from django import forms
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.conf import settings


importlib.import_module(getattr(
    settings, 'CELERY_TASKS_MODULE', 'dataplatform_sync.tasks'))

task_choices = list(
    sorted(
        (name, name) for name in current_app.tasks
        if not name.startswith('celery.')
    )
)


class TaskForm(forms.Form):
    delay = forms.BooleanField(required=False)
    task = forms.ChoiceField(choices=task_choices)

    def save(self):
        task = self.cleaned_data['task']
        args = self.cleaned_data.get('args', [])
        kwargs = self.cleaned_data.get('kwargs', {})
        delay = self.cleaned_data.get('delay')

        pos = task.rfind('.')
        task_name = task[pos + 1:]
        full_module_name = task[:pos]
        my_module = importlib.import_module(full_module_name)

        if delay:
            getattr(my_module, task_name).delay(*args, **kwargs)
        else:
            getattr(my_module, task_name)(*args, **kwargs)


class TaskView(FormView):
    form_class = TaskForm
    template_name = 'index.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
