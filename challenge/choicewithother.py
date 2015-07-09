from django.core.exceptions import ValidationError
from django import forms


class OptionalChoiceWidget(forms.MultiWidget):
    def decompress(self,value):
        if value:
            return [value[0],value[1]]
        return ["",""]

class OptionalChoiceField(forms.MultiValueField):
    def __init__(self, choices, max_length=200, *args, **kwargs):
        """ sets the two fields as not required but will enforce that (at least) one is set in compress """
        fields = (forms.ChoiceField(choices=choices,required=False),
                  forms.CharField(required=False))
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super(OptionalChoiceField,self).__init__(required=False,fields=fields,*args,**kwargs)
    def compress(self,data_list):
        """ return the choicefield value if selected or charfield value (if both empty, will throw exception """
        if not data_list:
            raise ValidationError('Need to select choice or enter text for this field')
        return data_list[0] or data_list[1]
