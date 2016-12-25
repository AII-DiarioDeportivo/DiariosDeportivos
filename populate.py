# encoding: utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DiariosDeportivos.settings'
import feedparser
from django.db.transaction import commit_on_success
from diarios_app.models import Noticia

#Clase de pruebas
@commit_on_success
def read_test():
    print "Populando de Marca..."
    parseo = feedparser.parse('http://estaticos.marca.com/rss/futbol/primera-division.xml')

    counter = 0
    for entrada in parseo.entries:
        print "Populando " + counter.__str__()
        id = counter
        counter+=1
        tit = entrada.title
        desc = entrada.content[0]['value']
        url_not = entrada.link
        foto = entrada.media_content[0]['url']
        fecha = entrada.published_parsed
        fech = fecha[0].__str__() + "-" + fecha[1].__str__() + "-" + fecha[2].__str__()

        noticia = Noticia(id_noticia=id, titulo = tit, descripcion = desc, url_foto = foto, url_noticia = url_not, fecha = fech)
        noticia.save()


if __name__ == "__main__":
    read_test()