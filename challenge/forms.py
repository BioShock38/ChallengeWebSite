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

    answer = forms.CharField(max_length=400)
    level = forms.ChoiceField(widget=forms.Select,
                              choices=Submission.LEVEL_CHOICES)

    with_environment_variable = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'Yes'), (True, 'No')),
        widget=forms.RadioSelect
    )

    software = forms.ModelChoiceField(Method.objects.all(), required=True)
    software_desc = forms.CharField(label="", widget=forms.Textarea,
                                    max_length=1000, required=False)