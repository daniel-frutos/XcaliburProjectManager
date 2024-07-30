from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Proposal, Responsible, Client, Project, BusinessUnit
from django.db.models import Q
from .forms import proposalform, responsibleform, clientform, projectform
from django.core.files import uploadedfile, File
from django.contrib import messages
from django.forms.models import model_to_dict
from shapely.geometry import Polygon, MultiPolygon, LineString
from lxml import etree



class MainView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect to the login page if the user is not authenticated

    def get(self, request):
        projects = Project.objects.all()
        act_proposallist = Proposal.objects.filter(Q(status='lead') | Q(status='proposal'))
        sig_proposallist = Proposal.objects.filter(status='signed')
        rej_proposallist = Proposal.objects.filter(Q(status='rejected') | Q(status='standby'))
        context = {'projects': projects, 'act_proposallist': act_proposallist,
                   'sig_proposallist': sig_proposallist,
                   'rej_proposallist': rej_proposallist}
        return render(request, 'projects/projects.html', context)


@login_required
def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        act_proposallist = Proposal.objects.filter(Q(status='lead') | Q(status='proposal'))
        sig_proposallist = Proposal.objects.filter(status='signed')
        rej_proposallist = Proposal.objects.filter(Q(status='rejected') | Q(status='standby'))
        context = {
            'user': request.user,
            'act_proposallist': act_proposallist,
            'sig_proposallist': sig_proposallist,
            'rej_proposallist': rej_proposallist,
        }
        return render(request, 'projects/projects.html', context)
    else:
        return redirect('/login/')


def extract_geometry_from_kml(kml_file_path):
    polygons = []
    with open(kml_file_path, 'rb') as f:
        tree = etree.parse(f)
        root = tree.getroot()
        ns = {'kml': 'http://www.opengis.net/kml/2.2'}
        for placemark in root.findall('.//kml:Placemark', namespaces=ns):
            # Extract geometry coordinates
            coordinates_str = placemark.find('.//kml:coordinates', namespaces=ns).text.strip()
            # Split coordinates string into individual points
            points = [tuple(map(float, point.split(',')[:2])) for point in coordinates_str.split()]

            # Check if the points are 2D or 3D
            if all(len(point) == 3 for point in points):
                # If 3D, create LineString and then Polygon
                linestring = LineString(points)
                polygon = Polygon(linestring)
            else:
                # If 2D, create Polygon directly
                polygon = Polygon(points)
            polygons.append(polygon)
    return MultiPolygon(polygons)

@login_required
def proposal_create_view(request):
    business_units = BusinessUnit.objects.all()
    if request.method == 'POST':
        form = proposalform(request.POST, request.FILES)
        files = request.FILES.getlist('uploads')

        if form.is_valid():
            obj = form.save(commit=False)
            files_num = 0

            for file in files:
                temp_file = uploadedfile.TemporaryUploadedFile.temporary_file_path(file)
                if files_num == len(files):
                    break
                else:
                    files_num += 1
                    obj.uploads.save(file.name, File(open(temp_file, 'rb')))

            form.save()

            if obj.coordinates:
                obj.geom = extract_geometry_from_kml(obj.coordinates.path).wkt
                obj.save()

            messages.success(request, 'Proposal created successfully!')
            return redirect('/projects/')
        else:
            # If the form is not valid, add error messages to the context
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = proposalform()

    context = {
        'form': form,
        'business_units': business_units,
    }
    return render(request, 'proposal/create.html', context)

"""
@login_required
def proposal_create_view(request):
    if request.method == 'POST':
        form = proposalform(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            # Save the form data
            obj.save()

            # Process the uploaded Shapefile(s)
            files = request.FILES.getlist('coordinates')  # Assuming 'coordinates' is the name of the file input field
            for shapefile in files:
                gdf = gpd.read_file(shapefile)
                geometry = gdf.geometry.to_json()
                # Save the geometry to the 'geom' field of the Project model
                obj.geom = geometry
                obj.save()  # Save the obj instance with the updated 'geom' field

            messages.success(request, 'Proposal created successfully!')
            return redirect('/projects/')
        else:
            context = {
                'form': form,
            }
            return render(request, 'proposal/create.html', context)
    else:
        form = proposalform()
        context = {
            'form': form,
        }
    return render(request, 'proposal/create.html', context)
"""


@login_required
def client_create_view(request):
    if request.method == 'POST':
        form = clientform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/client/create/')
        else:
            context = {
                'form': form,
            }
            return render(request, 'client/create.html', context)
    else:
        form = clientform()

        context = {
            'form': form,
        }
    return render(request, 'client/create.html', context)


@login_required
def proposal_update_view(request, id):
    obj = get_object_or_404(Proposal, id=id)
    form = proposalform(request.POST or None, instance=obj)
    if request.method == 'POST':
        form = proposalform(request.POST, request.FILES, instance=obj)
        files = request.FILES.getlist('uploads')
        if form.is_valid():
            obj = form.save(commit=False)
            # path = os.path.join(obj.country, datetime.now().strftime('%Y'),slugify(obj.title))
            files_num = 0
            for file in files:
                temp_file = uploadedfile.TemporaryUploadedFile.temporary_file_path(file)
                if files_num == (len(files)):
                    break
                else:
                    files_num += 1
                    obj.uploads.save(file.name, File(open(temp_file, 'rb')))
            form.save()
            if obj.coordinates:
                obj.geom = extract_geometry_from_kml(obj.coordinates.path).wkt
                obj.save()
            messages.success(request, 'Proposal updated successfully!')
            return redirect('/projects/')
        else:
            # If the form is not valid, add error messages to the context
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    context = {
        'form': form,
        'modify': 1,
    }
    return render(request, "proposal/create.html", context)


@login_required
def proposal_details_view(request, id):
    obj = get_object_or_404(Proposal, id=id)
    form = proposalform(request.POST or None, instance=obj)
    coords = []
    """for coor in obj.coordinates.splitlines():
        coords.append(parse_dms(coor))"""
    context = {
        #'coords': coords,
        'form': form,
    }
    return render(request, "proposal/details.html", context)


@login_required
def proposal_delete_view(request, id):
    obj = get_object_or_404(Proposal, id=id)
    if request.method == "POST":
        obj.delete()
        messages.error(request, 'Proposal deleted.')
        return redirect('/projects/')
    context = {
        'object': obj,
    }
    return render(request, 'proposal/delete.html', context)


@login_required
def responsible_create_view(request):
    if request.method == 'POST':
        form = responsibleform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/responsible/create/')
        else:
            context = {
                'form': form,
            }
            return render(request, 'responsible/create.html', context)
    else:
        form = responsibleform()

        context = {
            'form': form,
        }
    return render(request, 'responsible/create.html', context)


@login_required
def project_create_preview(request, id):
    prop = get_object_or_404(Proposal, id=id)
    init_data = model_to_dict(prop, exclude=['id', 'proposal_create_date', 'success_rate', 'status'])
    proj = Project()
    form = projectform(init_data, instance=proj)
    context = {'form': form, }
    if request.method == 'POST':
        form = projectform(request.POST, request.FILES, instance=proj)
        if form.is_valid():
            proj_form = form.save(commit=False)
            proj_form.proposal_fk = prop
            prop.locked = True
            prop.save()
            form.save()
            return redirect('/projects/')
    return render(request, 'project/create.html', context)

