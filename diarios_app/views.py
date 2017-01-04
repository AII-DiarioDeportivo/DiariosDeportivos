from diarios_app.models import Noticia,Puntuacion
from django.contrib.auth.models import User
import json
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from forms import RegistrationForm

def inicio(request):
    return render_to_response('inicio.html',context_instance=RequestContext(request))

@login_required
def primeraDivision(request):
    noticias = Noticia.objects.all()
    return render_to_response('primeraDivision.html', {'noticias': noticias, 'action':'/primeraDivision'},context_instance=RequestContext(request))

@login_required
def rate(request):
    if request.is_ajax():
        id_usuario = int(request.POST["id_usuario"])
        id_noticia = int(request.POST["id_noticia"])
        value = int(request.POST["value"])

        no = Noticia.objects.get(id_noticia=id_noticia)
        us = User.objects.get(id=id_usuario)
        print request.POST["id_noticia"]
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
