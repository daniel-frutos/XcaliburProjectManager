from django.contrib.gis.db import models
from django.core.validators import validate_comma_separated_integer_list, MaxValueValidator, MinValueValidator, \
    RegexValidator
from django.utils.text import slugify
# from django_mysql.models import ListTextField
import os
from datetime import datetime
from .country_codes import *
from re import split


# Create your models here.

class Responsible(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class Client(models.Model):
    client_type_choices = (
        ('government', 'Government'),
        ('major', 'Major Mining Comp'),
        ('junior', 'Junior Mining Comp'),
        ('oilgas', 'Oil & Gas'),
    )
    client_name = models.CharField(max_length=150, unique=True, default=None)
    client_type = models.CharField(max_length=30, choices=client_type_choices, default=None)
    client_abbrev = models.CharField(max_length=10, unique=True, default=None)

    def __str__(self):
        return self.client_name


class BusinessUnit(models.Model):
    bu_code = models.IntegerField(unique=True, blank=True, null=True)
    bu_name = models.CharField(max_length=150, unique=True, blank=True, null=True)

    def __str__(self):
        return self.bu_name


class Department(models.Model):
    dep_code = models.IntegerField(unique=True, blank=True, null=True)
    dep_name = models.CharField(max_length=150, unique=True, blank=True, null=True)

    def __str__(self):
        return self.dep_name


class Proposal(models.Model):
    status_choices = (
        ('proposal', 'Proposal'),
        ('lead', 'Lead'),
        # ('signed', 'Signed'),
        ('rejected', 'Rejected'),
        ('standby', 'Standby'),
    )
    financing_choices = (
        ('government', 'Government'),
        ('private', 'Private'),
        ('bilateral', 'Bilateral'),
        ('multilateral', 'Multilateral'),
        ('mixed', 'Mixed'),
    )
    country_choices = country_choices

    def upload_loc(self, filename):
        path = os.path.join('data/',self.country, datetime.now().strftime('%Y'), slugify(self.title), filename)
        return path


    # general info
    title = models.CharField(max_length=100, unique=False)
    reference = models.CharField(max_length=10, unique=False, blank=True, null=True)
    external_reference = models.CharField(max_length=50, unique=False, blank=True, null=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=50, choices=country_choices, default=None)
    color = models.CharField(max_length=15, unique=False, blank=True, null=True) #color for the polygon

    # country = models.CharField(max_length=50)
    # client_type = models.CharField(max_length=30, choices=client_type_choices)
    # client_name = models.CharField(max_length=150)
    client_name = models.ForeignKey(Client, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True)
    # client_type = models.ManyToManyField(Client, to_field='client_type', related_name='type', on_delete=models.DO_NOTHING, default=None)

    # economic info
    # budget = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    # financing_type = models.CharField(default=None, null=True, max_length=30, choices=financing_choices, blank=True)
    # financing = models.CharField(default=None, null=True, max_length=50, blank=True)

    # date info
    proposal_create_date = models.DateField(default=None, blank=True, null=True)
    project_start_date = models.DateField(default=None, blank=True, null=True)
    duration = models.DecimalField(default=None, null=True, max_digits=5, decimal_places=1, blank=True,
                                   verbose_name='Duration in months')

    # tech info
    gst = models.BooleanField(default=None, null=True, blank=True, verbose_name='Geospatial Technologies')
    fmagrad = models.BooleanField(default=None, null=True, blank=True, verbose_name='Airborne Magnetics & Radiometrics')
    hmagrad = models.BooleanField(default=None, null=True, blank=True, verbose_name='Helicopter Magnetics & Radiometrics')
    midas = models.BooleanField(default=None, null=True, blank=True, verbose_name='Helicopter Magnetics Gradient & Radiometrics')
    asg = models.BooleanField(default=None, null=True, blank=True, verbose_name='Airborne Scalar Gravity')
    fagg = models.BooleanField(default=None, blank=True, null=True, verbose_name='Airborne Gravity Gradiometer and Magnetic (Falcon)')
    hagg = models.BooleanField(default=None, blank=True, null=True, verbose_name='Helicopter Gravity Gradiometer and Magnetic (Falcon)')
    tempest = models.BooleanField(default=None, blank=True, null=True,
                               verbose_name='Airborne Time Domain Electromagnetic and Magnetic')
    helitem = models.BooleanField(default=None, blank=True, null=True,
                               verbose_name='Helicopter Time Domain Electromagnetic and Magnetic')
    proc_magrad = models.BooleanField(default=None, blank=True, null=True,
                               verbose_name='Magnetic and Radiometric Processing')
    others = models.BooleanField(default=None, blank=True, null=True, verbose_name='FTEM')
    #standard_grav_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
     #                                   validators=[validate_comma_separated_integer_list])
    #ftg_grav_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
     #                              validators=[validate_comma_separated_integer_list])
    #magnetometry_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
     #                                  validators=[validate_comma_separated_integer_list])
    #mag_grad_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
     #                             validators=[validate_comma_separated_integer_list])
    #spectrometry_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
     #                                  validators=[validate_comma_separated_integer_list])
    #hem_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
     #                         validators=[validate_comma_separated_integer_list])
    #ftem_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
      #                         validators=[validate_comma_separated_integer_list])
    others_desc = models.CharField(max_length=150, default=None, blank=True, null=True)

    # area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Area in km^2')
    coordinates = models.FileField(upload_to=upload_loc, blank=True, null=True)
    # coordinatesdd = models.FileField(upload_to=upload_loc, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    # contact info
    # in_charge = models.CharField(max_length=30, verbose_name='In charge of this proposal', choices=in_charge_choices, default=None)
    responsible = models.ForeignKey(Responsible, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True, related_name='responsible_1')
    responsible2 = models.ForeignKey(Responsible, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True, related_name='responsible_2')
    responsible3 = models.ForeignKey(Responsible, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True, related_name='responsible_3')
    foreign_contact = models.CharField(default=None, max_length=30, verbose_name='Foreign contact name', blank=True,
                                       null=True)
    foreign_contact_email = models.EmailField(default=None, max_length=100, verbose_name='Foreign contact email',
                                              blank=True, null=True)
    foreign_contact_phone = models.TextField(default=None, blank=True, null=True)

    # other info
    # success_rate = models.DecimalField(default=None, null=True, max_digits=5, decimal_places=2, blank=True,
      #                                 verbose_name='Success rate (base 1)')
    status = models.CharField(max_length=30, choices=status_choices)
    observations = models.TextField(max_length=150, blank=True)
    # uploads_loc = models.TextField(max_length=500, blank=True)
    # uploads = models.FileField(upload_to=upload_loc, blank=True, null=True)
    # upload4 = models.FileField(upload_to='%Y/%m/', blank=True, null=True)
    locked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-proposal_create_date']

    def __str__(self):
        return self.title

    def dms2dd(self, degrees, minutes, seconds, direction):
        dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60);
        if direction == 'S' or direction == 'W':
            dd *= -1
        return dd

    def parse_dms(self, dms):
        lat, lon = split(',', dms)
        partslat = split('[°\'"]+', lat)
        partslon = split('[°\'"]+', lon)
        finallat = self.dms2dd(partslat[0], partslat[1], partslat[2], partslat[3])
        finallon = self.dms2dd(partslon[0], partslon[1], partslon[2], partslon[3])
        return (finallat, finallon)


class Project(models.Model):
    financing_choices = (
        ('government', 'Government'),
        ('private', 'Private'),
        ('bilateral', 'Bilateral'),
        ('multilateral', 'Multilateral'),
        ('mixed', 'Mixed'),
    )
    country_choices = country_choices

    def upload_loc(self, filename):
        path = os.path.join(self.country, datetime.now().strftime('%Y'), slugify(self.title), filename)
        return path

    # general info
    title = models.CharField(max_length=100, unique=False)
    reference = models.CharField(max_length=10, unique=False, blank=True, null=True)
    external_reference = models.CharField(max_length=50, unique=False, blank=True, null=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=50, choices=country_choices)

    # country = models.CharField(max_length=50)
    # client_type = models.CharField(max_length=30, choices=client_type_choices)
    # client_name = models.CharField(max_length=150)
    client_name = models.ForeignKey(Client, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True)
    # client_type = models.ManyToManyField(Client, to_field='client_type', related_name='type', on_delete=models.DO_NOTHING, default=None)

    # economic info
    # budget = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    # financing_type = models.CharField(default=None, null=True, max_length=30, choices=financing_choices, blank=True)
    # financing = models.CharField(default=None, null=True, max_length=50, blank=True)

    # date info
    project_start_date = models.DateField(default=None, blank=True, null=True)
    duration = models.DecimalField(default=None, null=True, max_digits=5, decimal_places=1, blank=True,
                                   verbose_name='Duration in months')

    # tech info
    gst = models.BooleanField(default=None, null=True, blank=True, verbose_name='Geospatial Technologies')
    fmagrad = models.BooleanField(default=None, null=True, blank=True, verbose_name='Airborne Magnetics & Radiometrics')
    hmagrad = models.BooleanField(default=None, null=True, blank=True,
                                  verbose_name='Helicopter Magnetics & Radiometrics')
    midas = models.BooleanField(default=None, null=True, blank=True,
                                verbose_name='Helicopter Magnetics Gradient & Radiometrics')
    asg = models.BooleanField(default=None, null=True, blank=True, verbose_name='Airborne Scalar Gravity')
    fagg = models.BooleanField(default=None, blank=True, null=True,
                               verbose_name='Airborne Gravity Gradiometer and Magnetic (Falcon)')
    hagg = models.BooleanField(default=None, blank=True, null=True,
                               verbose_name='Helicopter Gravity Gradiometer and Magnetic (Falcon)')
    tempest = models.BooleanField(default=None, blank=True, null=True,
                                  verbose_name='Airborne Time Domain Electromagnetic and Magnetic')
    helitem = models.BooleanField(default=None, blank=True, null=True,
                                  verbose_name='Helicopter Time Domain Electromagnetic and Magnetic')
    proc_magrad = models.BooleanField(default=None, blank=True, null=True,
                                      verbose_name='Magnetic and Radiometric Processing')
    others = models.BooleanField(default=None, blank=True, null=True, verbose_name='FTEM')
    """standard_grav_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
                                        validators=[validate_comma_separated_integer_list])
    ftg_grav_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
                                   validators=[validate_comma_separated_integer_list])
    magnetometry_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
                                       validators=[validate_comma_separated_integer_list])
    mag_grad_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
                                   validators=[validate_comma_separated_integer_list])
    spectrometry_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
                                       validators=[validate_comma_separated_integer_list])
    hem_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
                              validators=[validate_comma_separated_integer_list])
    ftem_ls = models.CharField(max_length=30, default=None, blank=True, null=True,
                               validators=[validate_comma_separated_integer_list])"""
    others_desc = models.CharField(max_length=150, default=None, blank=True, null=True)

    # area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Area in km^2')
    coordinates = models.FileField(upload_to=upload_loc, blank=True, null=True)
    # coordinatesdd = models.FileField(upload_to=upload_loc, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    # contact info
    # in_charge = models.CharField(max_length=30, verbose_name='In charge of this proposal', choices=in_charge_choices, default=None)
    responsible = models.ForeignKey(Responsible, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True, related_name='proj_responsible_1')
    responsible2 = models.ForeignKey(Responsible, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True, related_name='proj_responsible_2')
    responsible3 = models.ForeignKey(Responsible, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True, related_name='proj_responsible_3')
    foreign_contact = models.CharField(default=None, max_length=30, verbose_name='Foreign contact name', blank=True,
                                       null=True)
    foreign_contact_email = models.EmailField(default=None, max_length=100, verbose_name='Foreign contact email',
                                              blank=True, null=True)
    foreign_contact_phone = models.TextField(default=None, blank=True, null=True)

    # other info
    observations = models.TextField(max_length=150, blank=True)
    # uploads_loc = models.TextField(max_length=500, blank=True)
    # uploads = models.FileField(upload_to=upload_loc, blank=True, null=True)
    # upload4 = models.FileField(upload_to='%Y/%m/', blank=True, null=True)

    proposal_fk = models.ForeignKey(Proposal, on_delete=models.SET_DEFAULT, null=True, default=None, blank=True)

    class Meta:
        ordering = ['-project_start_date']

    def __str__(self):
        return self.title

    def dms2dd(self, degrees, minutes, seconds, direction):
        dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60);
        if direction == 'S' or direction == 'W':
            dd *= -1
        return dd

    def parse_dms(self, dms):
        lat, lon = split(',', dms)
        partslat = split('[°\'"]+', lat)
        partslon = split('[°\'"]+', lon)
        finallat = self.dms2dd(partslat[0], partslat[1], partslat[2], partslat[3])
        finallon = self.dms2dd(partslon[0], partslon[1], partslon[2], partslon[3])
        return (finallat, finallon)

    """def save(self, *args, **kwargs):
        fixed_coords = []
        try:
            for pair in self.coordinates.splitlines():
                fixed_coords.append(self.parse_dms(pair))
        except:
            pass
        self.coordinatesdd = fixed_coords
        super(Project, self).save(*args, **kwargs)"""