from django import forms


class UploadSourceCodeForm(forms.Form):
    LANGUAGES = ['Python 3', 'Javascript']
    (LANGUAGE_PYTHON_3, LANGUAGE_JS) = range(2)
    language = forms.ChoiceField(choices=zip(range(len(LANGUAGES)), LANGUAGES))
    source_file = forms.FileField()
