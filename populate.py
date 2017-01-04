# encoding: utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DiariosDeportivos.settings'
import feedparser
import datetime
from django.db.transaction import commit_on_success
from diarios_app.models import Noticia
from django.utils.html import strip_tags
from django.db import models
from dateutil import parser
from django.utils import timezone

#Clase de pruebas
@commit_on_success
def read_primera_division_MARCA():
    print "Populando de Marca..."
    parseo = feedparser.parse('http://estaticos.marca.com/rss/futbol/primera-division.xml')

    #Tenemos que encontrar el ultimo id registrado
    if len(Noticia.objects.all()) == 0:
        counter = 1
        lastDate = datetime.datetime.today()
        lastDate = lastDate.replace(year=lastDate.year-3)
    else:
        counter = Noticia.objects.latest("id_noticia").id_noticia
        counter+=1
        lastDate = Noticia.objects.latest("fecha").fecha
        lastDate = lastDate.replace(hour=lastDate.hour + 1)

    for entrada in parseo.entries:
        id = counter
        counter+=1
        tit = entrada.title
        desc = entrada.content[0]['value']
        desc = strip_tags(desc)
        url_not = entrada.link
        foto = entrada.media_content[0]['url']
        fecha = entrada.published_parsed
        fech = fecha[0].__str__() + "-" + fecha[1].__str__() + "-" + fecha[2].__str__() + "-" + (fecha[3]+1).__str__() + ":" + fecha[4].__str__() + ":" + fecha[5].__str__()
        revista = "MARCA"

        fech2 = datetime.datetime.strptime(fech, "%Y-%m-%d-%H:%M:%S")

        lastDateStr = lastDate.__str__()[0:19]
        lastDate2 = datetime.datetime.strptime(lastDateStr.__str__(), "%Y-%m-%d %H:%M:%S")

        if fech2 > lastDate2:
            noticia = Noticia(id_noticia=id, titulo = tit, descripcion = desc, url_foto = foto, url_noticia = url_not, fecha = fech2, procedente_de=revista)
            noticia.save()

def prueba():
    print  len(Noticia.objects.all()).__str__()



if __name__ == "__main__":
    read_primera_division_MARCA()
    #prueba()