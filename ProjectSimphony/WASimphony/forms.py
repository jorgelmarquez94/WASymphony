
from django import forms
from WASimphony.models import SymphonyFileUpload

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = SymphonyFileUpload
        fields = ('document',)

