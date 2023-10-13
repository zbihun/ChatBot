from django import forms

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(
        widget=forms.FileInput(attrs={'id': 'audio-file-input'}), 
        required=False,
    )
