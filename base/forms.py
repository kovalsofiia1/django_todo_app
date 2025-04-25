# forms.py
from django import forms
from .models import Task, Collection

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'collection', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'border p-2 w-full mb-4 rounded',
                'placeholder': 'Назва задачі',
                'required': True
            }),
            'collection': forms.Select(attrs={
                'class': 'border p-2 w-full mb-4 rounded'
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border p-2 w-full mb-4 rounded'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['collection'].queryset = Collection.objects.filter(owner=user)
        self.fields['collection'].required = False
        self.fields['deadline'].required = False

