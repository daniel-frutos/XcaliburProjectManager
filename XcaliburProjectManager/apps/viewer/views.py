from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View


class Viewer(View):
    viewer_url = '/viewer/'  # Redirect to the login page if the user is not authenticated
    def get(self, request):
        return render(request, 'viewer/viewer_full.html')

