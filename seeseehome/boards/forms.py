"""
from django import forms
from ckeditor.fields import RichTextFormField
from ckeditor.widgets import CKEditorWidget

class WriteForm(forms.Form):
#   content = RichTextFormField()

#   For more Custom Client API, subject form was implemented 
#   in template(html)

#   This form is not used. It is just for reference 
    content = forms.CharField(
                  label="",
                  widget=CKEditorWidget(),
                  max_length = 65535,
              )
"""
