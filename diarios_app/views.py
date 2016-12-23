from django.shortcuts import render_to_response

def inicio(request):
    return render_to_response('inicio.html')