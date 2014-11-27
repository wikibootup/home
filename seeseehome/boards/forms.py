from django import forms
from ckeditor.fields import RichTextFormField
from ckeditor.widgets import CKEditorWidget

class WriteForm(forms.Form):
#   content = RichTextFormField()

#   For more Custom Client API, subject form was implemented 
#   in template(html)
    """
    subject = forms.CharField(
                  max_length = 255,
                  label="",
                  widget=forms.TextInput(
                      attrs={'placeholder': 'Enter Subject'},
                  ),
                  required = True,
              )
    """
    content = forms.CharField(
                  label="",
                  widget=CKEditorWidget(),
                  max_length = 65535,
              )

