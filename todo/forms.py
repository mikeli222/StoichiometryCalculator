from django import forms
from .views import Tasks
from users.models import Account



class TaskForm(forms.ModelForm):

    class Meta:
        model = Tasks
        fields = '__all__'


class CalculatorForm(forms.Form):
    reaction = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Enter a balanced reaction. Example: 2 H2 + O2 = 2 H2O',
        'size':'57','class':'form-control'}))
    given_amount = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Enter number', 'class':'form-control'}))
    CHOICES = [('grams', 'Grams'), ('moles', 'Moles'), ('molecules', 'Molecules')]
    given_units = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    given_formula = forms.CharField(required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Enter chemical formula', 'class': 'form-control'}))
    limiting = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'limiting-check'}))
    given_amount2 = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Enter number', 'class': 'form-control', 'id':'given_amount2'}))
    CHOICES = [('grams', 'Grams'), ('moles', 'Moles'), ('molecules', 'Molecules')]
    given_units2 = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    given_formula2 = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Enter chemical formula', 'class': 'form-control', 'id':'given_formula2' }))
    solving_units = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    solving_formula = forms.CharField(required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder':'Enter chemical '
                                                                                               'formula', 'class':'form-control'}))

    def clean_given_formula(self):
        reaction = self.cleaned_data.get('reaction')
        parsed = reaction.split(" ")
        parsed[:] = [x for x in parsed if x not in ["=", "+"]]
        i = 0
        while i < len(parsed):
            if not parsed[i].isdigit() and not parsed[i - 1].isdigit():
                parsed.insert(i, "1")
            i += 1
        given_formula = self.cleaned_data.get('given_formula')
        if given_formula not in parsed:
            raise forms.ValidationError(f'{given_formula} is not in the reaction')
        return given_formula

    def clean_solving_formula(self):
        reaction = self.cleaned_data.get('reaction')
        parsed = reaction.split(" ")
        parsed[:] = [x for x in parsed if x not in ["=", "+"]]
        i = 0
        while i < len(parsed):
            if not parsed[i].isdigit() and not parsed[i - 1].isdigit():
                parsed.insert(i, "1")
            i += 1
        solving_formula = self.cleaned_data.get('solving_formula')
        if solving_formula not in parsed:
            raise forms.ValidationError(f'{solving_formula} is not in the reaction')
        return solving_formula

    def clean_given_formula2(self):
        limiting = self.cleaned_data.get("limiting")
        if limiting:
            reaction = self.cleaned_data.get('reaction')
            parsed = reaction.split(" ")
            parsed[:] = [x for x in parsed if x not in ["=", "+"]]
            i = 0
            while i < len(parsed):
                if not parsed[i].isdigit() and not parsed[i - 1].isdigit():
                    parsed.insert(i, "1")
                i += 1
            given_formula = self.cleaned_data.get('given_formula')
            given_formula2 = self.cleaned_data.get('given_formula2')
            if given_formula2 not in parsed:
                raise forms.ValidationError(f'{given_formula2} is not in the reaction')
            if given_formula2 == given_formula:
                raise forms.ValidationError('First and second reactants can not be the same')
            return given_formula2