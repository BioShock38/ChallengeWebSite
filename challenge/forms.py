from django import forms
from .models import Submission, Dataset, Method
from .choicewithother import OptionalChoiceField

class SubmitForm(forms.Form):

    PRESENTED, OTHER = 'presented', 'other'
    METHOD_TYPE_CHOICES = (
        (PRESENTED, 'One of the presented methods'),
        (OTHER, 'Your own method'),
        )

    def __init__(self,data=None,*args,**kwargs):
        def conv(private):
            if private:
                return " (private Leaderboard)"
            else:
                return " (public Leaderboard)"
        l_simu = kwargs.pop("l_simu")
        super(SubmitForm,self).__init__(data,*args,**kwargs)
        self.fields['dataset'] = forms.ChoiceField(widget=forms.Select,
                                                   choices=[(simu.name,simu.name +
                                                             conv(simu.private)) for simu in l_simu])
        if data and data.get('softwaretype', None) == self.OTHER:
            self.fields['software_other'].required = True
        if data and data.get('softwaretype', None) == self.PRESENTED:
            self.fields['software_presented'].required = True


    answer = forms.CharField(max_length=400)
    level = forms.ChoiceField(widget=forms.Select,
                              choices=Submission.LEVEL_CHOICES)
    
    softwaretype = forms.ChoiceField(choices=METHOD_TYPE_CHOICES,
                                     widget=forms.RadioSelect)

    software_presented = forms.ModelChoiceField(Method.objects.all(), required=False)
    software_other = forms.CharField(label="", max_length=400, required=False)