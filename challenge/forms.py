from django import forms
from .models import Simulation

class SubmitForm(forms.Form):

    def __init__(self,*args,**kwargs):
        l_simu = kwargs.pop("l_simu")
        super(SubmitForm,self).__init__(*args,**kwargs)
        self.fields['select_simu'] = forms.ChoiceField(widget=forms.Select,
                                                       choices=[(simu.name,simu.name) for simu in l_simu])

    answer = forms.CharField(max_length=400)

    
