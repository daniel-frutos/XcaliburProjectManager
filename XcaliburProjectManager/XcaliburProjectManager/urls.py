"""
URL configuration for XcaliburProjectManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.login.views import LoginView, LogoutView
from apps.projects.views import MainView, proposal_create_view, client_create_view, proposal_update_view, proposal_delete_view, proposal_delete_view, responsible_create_view, project_create_preview, home_view, proposal_details_view
from apps.viewer.views import Viewer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('login/', LogoutView.as_view(), name='logout'),
    path('projects/', home_view, name='projects'),
    path('client/create/', client_create_view, name='client-create'),
    path('proposal/<int:id>/', proposal_details_view),
    path('proposal/<int:id>/update/', proposal_update_view, name='proposal-update'),
    path('proposal/<int:id>/delete/', proposal_delete_view, name='proposal-delete'),
    path('responsible/create/', responsible_create_view, name='responsible-create'),
    path('project/create/<int:id>/', project_create_preview, name='project-create-preview'),
    path('viewer/', Viewer.as_view(), name='viewer'),
    path('create/', proposal_create_view, name='create'),
]
