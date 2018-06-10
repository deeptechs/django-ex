from .models import Face, Photo, Album
from django import forms


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album

        fields = [
            'name',
        ]


class FaceForm(forms.ModelForm):
    class Meta:
        model = Face

        fields = [
            'x1',
            'x2',
            'y1',
            'y2',
            'identity_name',
            'feature',
        ]


class PhotoForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Photo

        fields = [
            'image',
        ]
