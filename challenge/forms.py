from django import forms
from .models import Submission, Dataset
from .choicewithother import OptionalChoiceField

class SubmitForm(forms.Form):

    def __init__(self,*args,**kwargs):
        def conv(private):
            if private:
                return " (private Leaderboard)"
            else:
                return " (public Leaderboard)"
        l_simu = kwargs.pop("l_simu")
        super(SubmitForm,self).__init__(*args,**kwargs)
        self.fields['dataset'] = forms.ChoiceField(widget=forms.Select,
                                                   choices=[(simu.name,simu.name + conv(simu.private)) for simu in l_simu])

    answer = forms.CharField(max_length=400)
    level = forms.ChoiceField(widget=forms.Select,
                              choices=Submission.LEVEL_CHOICES)
    software = OptionalChoiceField(choices=Submission.SOFTWARE_CHOICES)

    
