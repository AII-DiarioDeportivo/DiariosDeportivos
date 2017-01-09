from diarios_app.models import Noticia, Puntuacion, Etiquetas
from django.contrib.auth.models import User
import json
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from populate import read_futbol, read_moto, read_formula1, read_basket, indexar_datos

from diarios_app.services import  getRecommendations

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from forms import RegistrationForm

from whoosh.index import open_dir
from whoosh import qparser
from django.db.models import Count

def inicio(request):
    noticias = Noticia.objects.all().order_by('fecha').reverse()[:6]
    etiquetas = Etiquetas.objects.annotate(c=Count('noticias')).order_by('-c')[:5]

    etiquetas = sorted(set(etiquetas))

    noticias_recomendadas = None

    if request.user.is_authenticated() and len(request.user.puntuacion_set.all())!=0:
        prefs = create_prefs()
        tags = getRecommendations(prefs, request.user.pk)[:5]
        noticias_recomendadas = []
        for i in range(0, tags.__len__()):
            tag = Etiquetas.objects.get(id_etiqueta=tags[i][1])
            noticias_recomendadas.append(tag.noticias.all().order_by('fecha')[0])
    if not noticias_recomendadas:
        nr2 = []
    else:
        nr2 = list(set(noticias_recomendadas))
    return render_to_response('inicio.html',{'noticias': noticias, 'etiquetas':etiquetas, 'noticias_recomendadas':nr2},context_instance=RequestContext(request))

def populate(request):
    read_futbol()
    read_basket()
    read_formula1()
    read_moto()
    indexar_datos()

@login_required
def futbol(request):

    noticias = Noticia.objects.filter(deporte="FUTBOL").order_by("-fecha")
    paginator = Paginator(noticias, 12) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        noticias = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        noticias = paginator.page(paginator.num_pages)
    return render_to_response('noticias.html', {'noticias': noticias, 'action':'/futbol'},context_instance=RequestContext(request))

@login_required
def baloncesto(request):

    noticias = Noticia.objects.filter(deporte="BASKET").order_by("-fecha")
    paginator = Paginator(noticias, 12) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        noticias = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        noticias = paginator.page(paginator.num_pages)
    return render_to_response('noticias.html', {'noticias': noticias, 'action':'/baloncesto'},context_instance=RequestContext(request))


@login_required
def formula1(request):

    noticias = Noticia.objects.filter(deporte="F1").order_by("-fecha")
    paginator = Paginator(noticias, 12) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        noticias = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        noticias = paginator.page(paginator.num_pages)
    return render_to_response('noticias.html', {'noticias': noticias, 'action':'/formula1'},context_instance=RequestContext(request))

@login_required
def motociclismo(request):

    noticias = Noticia.objects.filter(deporte="MOTOCICLISMO").order_by("-fecha")
    paginator = Paginator(noticias, 12) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        noticias = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        noticias = paginator.page(paginator.num_pages)
    return render_to_response('noticias.html', {'noticias': noticias, 'action':'/motociclismo'},context_instance=RequestContext(request))




@login_required
def rate(request):
    if request.is_ajax():
        id_usuario = int(request.POST["id_usuario"])
        id_noticia = int(request.POST["id_noticia"])
        value = int(request.POST["value"])

        no = Noticia.objects.get(id_noticia=id_noticia)
        us = User.objects.get(id=id_usuario)
        try:
            ob = Puntuacion.objects.get(id_noticia=no.id_noticia ,id_usuario__username=us.username)
        except ObjectDoesNotExist:
            ob = None

        if ob!=None:
            ob.value = value
            ob.save()
        else:
            ob = Puntuacion(id_noticia=no, id_usuario=us ,value=value)
            ob.save()

        data = [{'id_usuario': id_usuario, 'id_noticia': id_noticia, 'value': value, 'id_p':ob.id}]
    return HttpResponse(json.dumps(data),content_type="application/json")

@login_required
def checkRate(request):
    if request.is_ajax():
        id_usuario = int(request.POST["id_usuario"])
        id_noticia = int(request.POST["id_noticia"])

        no = Noticia.objects.get(id_noticia=id_noticia)
        us = User.objects.get(id=id_usuario)
        try:
            ob = Puntuacion.objects.get(id_noticia=no.id_noticia ,id_usuario__username=us.username)
            data = [{'check':True, 'value':ob.value, 'id_noticia':id_noticia}]
        except ObjectDoesNotExist:
            ob = None
            data = [{'check': False, 'value': ob}]
    return HttpResponse(json.dumps(data),content_type="application/json")

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            user.save()

            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegistrationForm()

    return render_to_response('registration.html', {'form': form,}, context_instance=RequestContext(request))


# Busqueda con Whoosh

dirindexnoticias = "IndexNoticias"

def busca_noticias(request):

    noticia = request.GET.get('q', None)
    ix = open_dir(dirindexnoticias)

    with ix.searcher() as searcher:
        query = qparser.MultifieldParser(['titulo', 'descripcion', 'fecha'], ix.schema)
        q = query.parse(unicode(noticia))
        noticias = searcher.search(q)
        return render_to_response('inicio.html', {'noticias': noticias,}, context_instance=RequestContext(request))

def etiquetas_noticias(request):

    id_e = request.GET.get('q', None)

    etiqueta = Etiquetas.objects.filter(id_etiqueta=id_e)
    for e in etiqueta:
        etiqueta = e

    return render_to_response('inicio.html', {'noticias': etiqueta.noticias.all(),}, context_instance=RequestContext(request))





def create_prefs():
    puntuaciones = Puntuacion.objects.all()
    critics = {}
    for puntuacion in puntuaciones:
        for tag in puntuacion.id_noticia.etiquetas_set.all():
            user = puntuacion.id_usuario.pk
            etiqueta = tag.id_etiqueta.__str__()
            valor = puntuacion.value
            if user not in critics:
                critics[user] = {}
            critics[user][etiqueta] = valor

    return critics
