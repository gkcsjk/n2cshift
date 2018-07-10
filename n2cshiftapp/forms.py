# coding=utf-8
from django import forms
from n2cshiftapp import myutils


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        error_messages={'required': 'Input your username'},
        widget=forms.TextInput(attrs={'class': 'w3-input w3-border'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
        error_messages={'required': 'Input your password'}
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("You must input your username and password")
        else:
            cleaned_data = super(LoginForm, self).clean()


class ShiftForm(forms.Form):
    date = forms.DateField(
        required=True,
        # label='Date (eg.2017-11-11)',
        widget=forms.DateInput(attrs={'class': 'w3-input w3-border', 'id': "datepicker"})
    )
    shift = forms.ChoiceField(
        required=True,
        choices= (
            ('Morning', '早班'),
            ('Dusk', '晚班'),
            ('Night', '夜班'),
        ),
        widget=forms.Select(attrs={'class': 'w3-input w3-border'})
    )
    machine = forms.DecimalField(
        required=True,
        # label='Machine',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w3-input w3-border'})
    )
    cash = forms.DecimalField(
        required=True,
        # label='Cash',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w3-input w3-border'})
    )
    cards = forms.DecimalField(
        required=True,
        # label='Cards',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w3-input w3-border'})
    )
    cards_dtl = forms.CharField(
        # label='Details of Card',
        widget=forms.TextInput(attrs={'class': 'w3-input w3-border'})
    )
    receipts = forms.DecimalField(
        # label='Receipts',
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w3-input w3-border'})
    )
    receipts_dtl = forms.CharField(
        # label='Details of receipts',
        widget=forms.TextInput(attrs={'class': 'w3-input w3-border'})
    )
    IOUs = forms.DecimalField(
        # label='IOUs',
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w3-input w3-border'})
    )
    IOUs_dtl = forms.CharField(
        # label='Details of IOUs',
        widget=forms.TextInput(attrs={'class': 'w3-input w3-border'})
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("Input is Invalid!")
        else:
            cleaned_data = super(ShiftForm, self).clean()


class QueryForm(forms.Form):
    staff = forms.ChoiceField(
        # label='Choose staff',
        required=False,
        choices=myutils.list_user_to_tuple(),
        widget=forms.Select(attrs={'class': 'w3-input w3-border'})
    )
    start_date = forms.DateField(
        required=True,
        # label='Start date'
        widget=forms.DateInput(attrs={'class': 'w3-input w3-border', 'id': "datepicker"})
    )
    end_date = forms.DateField(
        required=False,
        # label='End date'
        widget=forms.DateInput(attrs={'class': 'w3-input w3-border', 'id': "datepicker1"})
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("Input is Invalid!")
        else:
            cleaned_data = super(QueryForm, self).clean()


class ChangePWForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        # label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
    )
    new_password = forms.CharField(
        required=True,
        # label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
    )
    new_password_2 = forms.CharField(
        required=True,
        # label='New Password Again',
        widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("Input is Invalid!")
        else:
            cleaned_data = super(ChangePWForm, self).clean()


class StaffQueryForm(forms.Form):
    start_date = forms.DateField(
        # label='From',
        required=False,
        widget=forms.DateInput(attrs={'class': 'w3-input w3-border', 'id': "datepicker"})
    )
    end_date = forms.DateField(
        # label='To',
        required=False,
        widget=forms.DateInput(attrs={'class': 'w3-input w3-border', 'id': "datepicker1"})
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("Input is Invalid!")
        else:
            cleaned_data = super(StaffQueryForm, self).clean()


# How much to pay
class SearchSalaryForm(forms.Form):
    start_date = forms.DateField(
        required=True,
        # label='Start Date'
        widget=forms.DateInput(attrs={'class': 'w3-input w3-border', 'id': "datepicker"})
    )
    type = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'w3-check'})
    )
    change_total_to = forms.DecimalField(
        required=False,
        # label='Change Total To:'
        widget=forms.NumberInput(attrs={'class': 'w3-input w3-border'})
    )
    comments = forms.CharField(
        # label="Comments",
        required=False,
        widget=forms.TextInput(attrs={'class': 'w3-input w3-border'})
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("Input is Invalid!")
        else:
            cleaned_data = super(SearchSalaryForm, self).clean()


# How much paid
class QuerySalaryForm(forms.Form):
    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'w3-input w3-border', 'id': "datepicker"})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'w3-input w3-border', 'id': "datepicker1"})
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("Input is Invalid!")
        else:
            cleaned_data = super(QuerySalaryForm, self).clean()

