from django import forms
from django.contrib.admin import widgets
from .models import Proposal

class proposalform(forms.ModelForm):
	standard_grav = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'check_standard_grav()'}))
	ftg_grav = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'check_ftg_grav()'}))
	magnetometry = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'check_magnetometry()'}))
	mag_grad = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'check_mag_grad()'}))
	spectrometry = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'check_spectrometry()'}))
	hem = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'check_hem()'}))
	ftem = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'check_ftem()'}))



	class Meta:
		model = Proposal
		fields = [
			'title', 
			'description',
			'country',
			'client_type',
			'client_name',
			#--
			'budget',
			'financing_type',
			'financing',
			#--
			'presentation_date',
			'start_date',
			'duration',
			#--
			'standard_grav',
			'standard_grav_ls',
			'ftg_grav',
			'ftg_grav_ls',
			'magnetometry',
			'magnetometry_ls',
			'mag_grad',
			'mag_grad_ls',
			'spectrometry',
			'spectrometry_ls',
			'hem',
			'hem_ls',
			'ftem',
			'ftem_ls',
			#--
			'area',
			'coordinates_x',
			'coordinates_y',
			#--
			'in_charge',
			'foreign_contact',
			#--
			'success_rate',
			'status',
			'observations',
			'uploads',

		]
		widgets = {
					'standard_grav_ls': forms.TextInput(attrs={'disabled': True}),
					'ftg_grav_ls': forms.TextInput(attrs={'disabled': True}),
					'magnetometry_ls': forms.TextInput(attrs={'readonly': True}),
					'mag_grad_ls': forms.TextInput(attrs={'readonly': True}),
					'spectrometry_ls': forms.TextInput(attrs={'readonly': True}),
					'hem_ls': forms.TextInput(attrs={'readonly': True}),
					'ftem_ls': forms.TextInput(attrs={'readonly': True}),

				}

		#exclude = ['standard_grav_ls', 'ftg_grav_ls','ftg_grav_ls','magnetometry_ls','mag_grad_ls','spectrometry_ls','hem_ls','ftem_ls',]
