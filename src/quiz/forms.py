from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Exam, Question, Choice


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'score']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class BaseChoiceFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        correct_count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct'):
                    correct_count += 1

        if correct_count != 1:
            raise ValidationError("Exactly one option must be marked as correct.")


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=['text', 'is_correct'],
    extra=4,
    can_delete=False,
    formset=BaseChoiceFormSet
)