from django import forms
from django.utils.translation import gettext_lazy as _

from tags.models import Tag

from .models import Post


class CreatePostModelForm(forms.ModelForm):
    title = forms.CharField(label=_('Title'), widget=forms.TextInput(
        attrs={'placeholder': _('Title'), 'class': 'form-control col-sm-12'}))
    text = forms.CharField(label=_('Text'), widget=forms.Textarea(
        attrs={'placeholder': _('Enter content of article'), 'class': 'form-control col-sm-6', 'rows': '20'}))
    tag = forms.CharField(label=_('Tag'), required=False, widget=forms.TextInput(
        attrs={'placeholder': _('Enter up to 5 tags separated by spaces.'), 'class': 'col-sm-12 form-control'}))

    def clean(self, *args, **kwargs):
        cleaned_tag = self.cleaned_data.get('tag')
        if not cleaned_tag:
            self.cleaned_data.pop('tag')
        else:
            tag_list = cleaned_tag.split(' ')
            if len(tag_list) >= 6:
                raise forms.ValidationError(_("Up to five tags can be registered."))
            for index, tag in enumerate(tag_list, start=1):
                Tag.objects.get_or_create(tag=tag)

        return self.cleaned_data

    class Meta:
        model = Post
        fields = ['title', 'text', 'tag']


class UpdatePostModelForm(CreatePostModelForm):
    id = forms.IntegerField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'text', 'tag', 'id']