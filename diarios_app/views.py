from diarios_app.models import Noticia
from django.shortcuts import render_to_response

def inicio(request):
    return render_to_response('inicio.html')

def noticias(request):
    noticias = Noticia.objects.all()
    return render_to_response('noticias.html', {'noticias': noticias})