from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DiariosDeportivos.views.home', name='home'),
    # url(r'^DiariosDeportivos/', include('DiariosDeportivos.foo.urls')),

    url(r'^$', 'diarios_app.views.inicio', name='home'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^primeraDivision/$', 'diarios_app.views.primeraDivision'),

    url(r'^registration$', 'diarios_app.views.registration', name='registration'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html', }, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('home'), }, name="logout"),

    url(r'^rate/$', 'diarios_app.views.rate'),
    url(r'^check_rate/$', 'diarios_app.views.checkRate'),

    url(r'^search/$', 'diarios_app.views.busca_noticias', name="search"),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
