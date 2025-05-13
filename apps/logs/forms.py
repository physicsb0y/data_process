from django import forms

from apps.logs.models import FileUploadTrack


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUploadTrack
        fields = ['file']

        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.xlsx, .xls, .csv'
            })
        }

        labels = {
            'file': 'Upload File'
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        print("File: ", file)
        allowed_extensions = ('.xlsx', '.xls', '.csv')
        if not file.name.lower().endswith(allowed_extensions):
            self.add_error('file', 'Unsupported file format')
        return file

