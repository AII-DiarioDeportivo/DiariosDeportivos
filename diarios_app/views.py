from diarios_app.models import Noticia
from django.shortcuts import render_to_response

def inicio(request):
    return render_to_response('inicio.html')

def primeraDivision(request):
    noticias = Noticia.objects.all()
    return render_to_response('primeraDivision.html', {'noticias': noticias, 'action':'/primeraDivision'})