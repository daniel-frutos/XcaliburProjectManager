from django import forms
from django.contrib.admin import widgets
from .models import Responsible, Proposal, Client, Project
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import validate_comma_separated_integer_list
from .country_codes import *

status_choices = (
	('lead', 'Lead'),
	('proposal', 'Proposal'),
	# ('signed', 'Signed'),
	('rejected', 'Rejected'),
	('standby', 'Standby'),
)
financing_choices = (
    ('', ''),
    ('government', 'Government'),
    ('private', 'Private'),
    ('bilateral', 'Bilateral'),
    ('multilateral', 'Multilateral'),
    ('mixed', 'Mixed'),
)
country_choices = country_choices


class proposalform(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ['upload4', ]

    # BASIC INFO
    title = forms.CharField(
        max_length=100,
        label='Title',
        widget=forms.TextInput(attrs={'placeholder': 'Proposal name or title'}),
    )
    reference = forms.CharField(
        max_length=10,
        label='Reference',
        widget=forms.TextInput(attrs={'placeholder': 'Internal reference'}),
    )
    external_reference = forms.CharField(
        max_length=50,
        label='External Reference',
        widget=forms.TextInput(attrs={'placeholder': 'External reference'}),
    )
    # country = forms.CharField(
    # 	max_length = 100,
    # 	label = 'Country',
    # 	widget = forms.TextInput(attrs={'placeholder': 'Country'}),
    # 	)
    country = forms.ChoiceField(
        choices=country_choices,
        required=True,
    )

    description = forms.CharField(
        required=False,
        max_length=2000,
        label='Proposal description',
        widget=forms.Textarea(),
    )

    # CLIENT INFO
    # client_name = forms.CharField(
    # 	max_length=150,
    # 	label = 'Client/Company name',
    # 	)
    client_name = forms.ModelChoiceField(
        queryset=Client.objects.all()
    )

    # client_type = forms.ChoiceField(
    # 	choices=client_type_choices,
    # 	label = 'Client type',
    # 	)

    # ECONOMIC INFO
    budget = forms.DecimalField(
        min_value=0,
        # widget = forms.NumberInput(attrs={'placeholder': 'Budget in millions'}),
        widget=forms.TextInput(attrs={'placeholder': 'Budget in millions'}),
        max_digits=50,
        decimal_places=3,
        required=False,
    )

    financing = forms.CharField(
        required=False,
        max_length=50,
        label='Financing Entity',
        widget=forms.TextInput(attrs={'placeholder': 'Financing Entity'}),
    )
    financing_type = forms.ChoiceField(
        choices=financing_choices,
        required=False,
    )

    # DATE INFO
    proposal_create_date = forms.DateField(
        label='Proposal created/modified',
        widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY', 'disabled': 'true'}),
        required=False,
    )
    project_start_date = forms.DateField(
        label='Project start date',
        widget=forms.TextInput(attrs={'id': 'datepicker', 'class': 'datepicker', 'placeholder': 'MM/DD/YYYY'}),
        required=False,
    )
    duration = forms.DecimalField(
        min_value=0,
        label='Project duration',
        widget=forms.NumberInput(attrs={'placeholder': 'Duration in months'}),
        max_digits=6,
        decimal_places=1,
        required=False,
    )

    # TECH INFO
    standard_grav = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_standard_grav()'}),
        label='GRAV'
    )
    ftg_grav = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_ftg_grav()'}),
        label='FTG'

    )
    magnetometry = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_magnetometry()'}),
        label='MAG'
    )
    mag_grad = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_mag_grad()'}),
        label='GRADMAG',
    )
    spectrometry = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_spectrometry()'}),
        label='RAD'
    )
    hem = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_hem()'}),
        label='HEM'
    )
    ftem = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_ftem()'}),
        label='FTEM'
    )
    others = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_others()'}),
        label='Others'
    )

    standard_grav_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    ftg_grav_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    magnetometry_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    mag_grad_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    spectrometry_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    hem_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    ftem_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    others_desc = forms.CharField(
        required=False,
        max_length=150,
        label='',
        widget=forms.TextInput(attrs={'disabled': True}),
    )

    coordinates = forms.FileField(
        widget=forms.FileInput(),
        label='Upload kml',
        required=False,
    )

    area = forms.DecimalField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Area in km^2'}),
        max_digits=10,
        decimal_places=2,
        required=False,
    )
    responsible = forms.ModelChoiceField(
        queryset=Responsible.objects.all()
    )
    responsible2 = forms.ModelChoiceField(
        queryset=Responsible.objects.all(),
        required=False,
    )
    responsible3 = forms.ModelChoiceField(
        queryset=Responsible.objects.all(),
        required=False,
    )
    foreign_contact = forms.CharField(
        required=False,
        max_length=30,
        label='Client contact name',
    )
    foreign_contact_email = forms.EmailField(
        required=False,
        max_length=100,
        label='Client email',
    )
    foreign_contact_phone = PhoneNumberField(
        required=False,
        label='Client phone number',
        widget=forms.TextInput(attrs={'placeholder': '+XX XXXXXXXXX'}),
    )

    # OTHER INFO
    success_rate = forms.DecimalField(
        max_digits=5,
        max_value=1,
        decimal_places=2,
        required=False,
        label='Success Rate',
        widget=forms.NumberInput(attrs={'placeholder': 'Base 1'}),
    )
    status = forms.ChoiceField(
        choices=status_choices,
        label='Proposal status',
    )
    observations = forms.CharField(
        required=False,
        max_length=2000,
        widget=forms.Textarea(),
    )

    # FILES#
    # upload1 = forms.FileField(
    # 	widget = forms.ClearableFileInput(),
    # 	label = 'Upload relevant doc',
    # 	required = False,
    # 	)
    uploads = forms.FileField(
        widget=forms.FileInput(),
        label='Upload relevant docs',
        required=False,
    )


class responsibleform(forms.ModelForm):
    class Meta:
        model = Responsible
        fields = ['name']

    name = forms.CharField(
        max_length=150,
        label='Input full name',
        widget=forms.TextInput(attrs={'placeholder': 'Full name'}),
    )


class clientform(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name', 'client_type', 'client_abbrev']


class projectform(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['upload4', ]

    # BASIC INFO
    title = forms.CharField(
        max_length=100,
        label='Title',
        widget=forms.TextInput(attrs={'placeholder': 'Proposal name or title'}),
    )

    reference = forms.CharField(
        max_length=10,
        label='Internal Reference',
        widget=forms.TextInput(attrs={'placeholder': 'Internal reference'}),
    )

    external_reference = forms.CharField(
        max_length=50,
        label='External Reference',
        widget=forms.TextInput(attrs={'placeholder': 'External reference'}),
    )
    # country = forms.CharField(
    # 	max_length = 100,
    # 	label = 'Country',
    # 	widget = forms.TextInput(attrs={'placeholder': 'Country'}),
    # 	)
    country = forms.ChoiceField(
        choices=country_choices,
        required=True,
    )

    description = forms.CharField(
        required=False,
        max_length=2000,
        label='Proposal description',
        widget=forms.Textarea(),
    )

    # CLIENT INFO
    # client_name = forms.CharField(
    # 	max_length=150,
    # 	label = 'Client/Company name',
    # 	)
    client_name = forms.ModelChoiceField(
        queryset=Client.objects.all()
    )

    # client_type = forms.ChoiceField(
    # 	choices=client_type_choices,
    # 	label = 'Client type',
    # 	)

    # ECONOMIC INFO
    budget = forms.DecimalField(
        min_value=0,
        # widget = forms.NumberInput(attrs={'placeholder': 'Budget in millions'}),
        widget=forms.TextInput(attrs={'placeholder': 'Budget in millions'}),
        max_digits=50,
        decimal_places=3,
        required=False,
    )

    financing = forms.CharField(
        required=False,
        max_length=50,
        label='Financing Entity',
        widget=forms.TextInput(attrs={'placeholder': 'Financing Entity'}),
    )
    financing_type = forms.ChoiceField(
        choices=financing_choices,
        required=False,
    )

    # DATE INFO
    project_start_date = forms.DateField(
        label='Project start date',
        widget=forms.TextInput(attrs={'id': 'datepicker', 'class': 'datepicker', 'placeholder': 'MM/DD/YYYY'}),
        required=False,
    )
    duration = forms.DecimalField(
        min_value=0,
        label='Project duration',
        widget=forms.NumberInput(attrs={'placeholder': 'Duration in months'}),
        max_digits=6,
        decimal_places=1,
        required=False,
    )

    # TECH INFO
    standard_grav = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_standard_grav()'}),
        label='GRAV'
    )
    ftg_grav = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_ftg_grav()'}),
        label='FTG'

    )
    magnetometry = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_magnetometry()'}),
        label='MAG'
    )
    mag_grad = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_mag_grad()'}),
        label='GRADMAG',
    )
    spectrometry = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_spectrometry()'}),
        label='RAD'
    )
    hem = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_hem()'}),
        label='HEM'
    )
    ftem = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_ftem()'}),
        label='FTEM'
    )
    others = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'onclick': 'check_others()'}),
        label='Others'
    )

    standard_grav_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    ftg_grav_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    magnetometry_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    mag_grad_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    spectrometry_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    hem_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    ftem_ls = forms.CharField(
        required=False,
        label='',
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(attrs={'placeholder': 'LS in meters', 'disabled': True}),
    )
    others_desc = forms.CharField(
        required=False,
        max_length=150,
        label='',
        widget=forms.TextInput(attrs={'disabled': True}),
    )

    coordinates = forms.FileField(
        widget=forms.FileInput(),
        label='Upload kml',
        required=False,
    )


    area = forms.DecimalField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Area in km^2'}),
        max_digits=10,
        decimal_places=2,
        required=False,
    )
    responsible = forms.ModelChoiceField(
        queryset=Responsible.objects.all()
    )
    responsible2 = forms.ModelChoiceField(
        queryset=Responsible.objects.all()
    )
    responsible3 = forms.ModelChoiceField(
        queryset=Responsible.objects.all()
    )
    foreign_contact = forms.CharField(
        required=False,
        max_length=30,
        label='Client contact name',
    )
    foreign_contact_email = forms.EmailField(
        required=False,
        max_length=100,
        label='Client email',
    )
    foreign_contact_phone = PhoneNumberField(
        required=False,
        label='Client phone number',
        widget=forms.TextInput(attrs={'placeholder': '+XX XXXXXXXXX'}),
    )

    # OTHER INFO
    observations = forms.CharField(
        required=False,
        max_length=2000,
        widget=forms.Textarea(),
    )

    # FILES#
    # upload1 = forms.FileField(
    # 	widget = forms.ClearableFileInput(),
    # 	label = 'Upload relevant doc',
    # 	required = False,
    # 	)
    uploads = forms.FileField(
        widget=forms.FileInput(),
        label='Upload relevant docs',
        required=False,
    )











