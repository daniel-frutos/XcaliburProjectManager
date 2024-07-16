from django.contrib import admin

# Register your models here.

from .models import Proposal, Responsible, Client, Project

# class ProposalAdmin(admin.ModelAdmin):
# 	fieldsets = (
# 		('General Info', {
# 			'fields':('title', 'description', 'country', ('client_name', 'client_type'),)
# 			}),
# 		('Economic Info', {
# 			'classes': ('collapse',),
# 			'fields':('budget','financing_type','financing',)
# 			}),
# 		('Date Info', {
# 			'classes': ('collapse',),
# 			'fields':('presentation_date','start_date', 'duration',)
# 			}),
# 		('Tech Info', {
# 			'classes': ('wide',),
# 			'fields':(
# 				('standard_grav','standard_grav_ls'),
# 				('ftg_grav','ftg_grav_ls'),
# 				('magnetometry','magnetometry_ls'),
# 				('mag_grad','mag_grad_ls'),
# 				('spectrometry','spectrometry_ls'),
# 				('hem','hem_ls'),
# 				('ftem','ftem_ls'),
# 				'area',
# 				'coordinates_x',
# 				'coordinates_y',
# 				)}),
# 		('Contact Info', {
# 			'fields':('in_charge','foreign_contact',)
# 			}),
# 		('Other Info', {
# 			'fields':('success_rate','status','observations','uploads',)
# 			}),
# 		)

#admin.site.register (Proposal, ProposalAdmin)
admin.site.register ([Proposal, Responsible, Client, Project])