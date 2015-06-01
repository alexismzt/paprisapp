"""paprisapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from helpdesk.views import HomeIndexView, ServiciosView, ServicioCreateNew, ServicioDetailView, CoordinacionTecnicaListView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'helpdesk.views.login', name='login'),
    url(r'^logout$', 'helpdesk.views.logout', name='logout'),  
    url(r'^$',HomeIndexView.as_view(), name='HomeIndex'),
    url(r'^helpdesk/servicios/$', ServiciosView.as_view(), name='ServiciosIndex'),
    url(r'^helpdesk/servicioNew/(?P<codigo>[\w]+)$', ServicioCreateNew.as_view(), name='ServicioCreateNewIndex'),
    url(r'^helpdesk/ServicioDetails/(?P<pk>[\w]+)$', ServicioDetailView.as_view(), name='ServicioDetailIndex'),
    url(r'^helpdesk/coordinacion$', CoordinacionTecnicaListView.as_view(), name='CoordinacionTecnicaIndex'),
]
