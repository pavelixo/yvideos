from django import forms

from .models import Video

class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "media"]
        labels = {
            "title": "Título",
            "media": "Vídeo",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500",
                "placeholder": "Digite o título do vídeo"
            }),
            "media": forms.ClearableFileInput(attrs={
                "class": "w-full text-white bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-orange-500",
            }),
        }