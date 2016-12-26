from diarios_app.models import Noticia
from django.contrib.auth.models import User

from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required

from forms import RegistrationForm

def inicio(request):
    return render_to_response('inicio.html',context_instance=RequestContext(request))

@login_required
def primeraDivision(request):
    noticias = Noticia.objects.all()
    return render_to_response('primeraDivision.html', {'noticias': noticias, 'action':'/primeraDivision'},context_instance=RequestContext(request))


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
