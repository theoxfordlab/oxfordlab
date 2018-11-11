"""oxfordlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from users import views
from django.conf import settings
from django.conf.urls.static import static
from manage_urls import views as manage_view

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^manage_urls/$', manage_view.manage_urls, name='manage_urls'),
    url(r'^signup/', views.registration, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^add_new_url/$', manage_view.add_new_url, name='add_new_url'),
    url(r'^add_new_group/$', manage_view.add_new_group, name='add_new_group'),
    url(
        r'^update_url_group/$',
        manage_view.update_url_group,
        name='update_url_group'
    ),
    url(
        r'^add_new_url_extension/$',
        manage_view.add_new_url_extension,
        name='add_new_url_extension',
    ),
    url(r'^$', views.home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)