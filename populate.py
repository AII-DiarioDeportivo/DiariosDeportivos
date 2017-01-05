# encoding: utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DiariosDeportivos.settings'
import feedparser
import datetime
from django.db.transaction import commit_on_success
from diarios_app.models import Noticia, Etiquetas
from django.utils.html import strip_tags
from django.db import models
from dateutil import parser
from django.utils import timezone
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, KEYWORD, ID, NUMERIC, DATETIME
import sqlite3


#EXTRACCIÓN DE DATOS DE MARCA - FUTBOL
@commit_on_success
def read_primera_division_MARCA():
    print "Populando FUTBOL de Marca..."
    parseo = feedparser.parse('http://estaticos.marca.com/rss/futbol/primera-division.xml')

    # Tenemos que encontrar el ultimo id registrado
    if len(Noticia.objects.all()) == 0:
        counter = 1
        lastDate = datetime.datetime.today()
        lastDate = lastDate.replace(year=lastDate.year - 3)
    else:
        if "MARCA-FUTBOL" not in Noticia.objects.values_list('procedente_de', flat=True):
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter += 1
            lastDate = datetime.datetime.today()
            lastDate = lastDate.replace(year=lastDate.year - 3)

        else:
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter += 1
            queryset = Noticia.objects.filter(procedente_de='MARCA-FUTBOL')
            lastDate = queryset.latest("fecha").fecha
            lastDate = lastDate.replace(hour=lastDate.hour + 1)

    for entrada in parseo.entries:
        revista = "MARCA-FUTBOL"
        _deporte = "FUTBOL"
        id = counter
        counter+=1
        tit = entrada.title
        desc = entrada.content[0]['value']
        desc = strip_tags(desc)
        desc = desc[0:150]
        url_not = entrada.link
        foto = entrada.media_content[0]['url']

        fecha = entrada.published_parsed
        fech = fecha[0].__str__() + "-" + fecha[1].__str__() + "-" + fecha[2].__str__() + "-" + (fecha[3]+1).__str__() + ":" + fecha[4].__str__() + ":" + fecha[5].__str__()
        fech2 = datetime.datetime.strptime(fech, "%Y-%m-%d-%H:%M:%S")
        lastDateStr = lastDate.__str__()[0:19]
        lastDate2 = datetime.datetime.strptime(lastDateStr.__str__(), "%Y-%m-%d %H:%M:%S")

        if fech2 > lastDate2:
            noticia = Noticia(id_noticia=id, titulo = tit, descripcion = desc, url_foto = foto, url_noticia = url_not, fecha = fech2, procedente_de=revista, deporte=_deporte)
            noticia.save()

            for t in entrada.tags:
                try:
                    etiquetas = Etiquetas.objects.all()
                    if t['term'] in Etiquetas.objects.values_list('nombre', flat=True):
                        etiqueta = Etiquetas.objects.get(nombre=t['term'])
                        etiqueta.noticias.add(noticia)
                    else:
                        id = len(Etiquetas.objects.all())
                        name = t['term']
                        etiqueta = Etiquetas(id_etiqueta=id, nombre=name)
                        etiqueta.save()
                        etiqueta.noticias.add(noticia)
                except:
                    print ""

# EXTRACCIÓN DE DATOS DE MARCA - BASKET
@commit_on_success
def read_liga_endesa_MARCA():
    print "Populando BASKET de Marca..."
    parseo = feedparser.parse('http://estaticos.marca.com/rss/baloncesto/acb.xml')

    # Tenemos que encontrar el ultimo id registrado
    if len(Noticia.objects.all()) == 0:
        counter = 1
        lastDate = datetime.datetime.today()
        lastDate = lastDate.replace(year=lastDate.year - 3)
    else:
        if "MARCA-BASKET" not in Noticia.objects.values_list('procedente_de', flat=True):
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter += 1
            lastDate = datetime.datetime.today()
            lastDate = lastDate.replace(year=lastDate.year - 3)
        else:
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter += 1
            queryset = Noticia.objects.filter(procedente_de='MARCA-BASKET')
            lastDate = queryset.latest("fecha").fecha
            lastDate = lastDate.replace(hour=lastDate.hour + 1)

    for entrada in parseo.entries:
        revista = "MARCA-BASKET"
        _deporte = "BASKET"
        id = counter
        counter += 1
        tit = entrada.title
        desc = entrada.content[0]['value']
        desc = strip_tags(desc)
        desc = desc[0:150]
        url_not = entrada.link
        foto = entrada.media_content[0]['url']

        fecha = entrada.published_parsed
        fech = fecha[0].__str__() + "-" + fecha[1].__str__() + "-" + fecha[2].__str__() + "-" + (fecha[3]).__str__() + ":" + fecha[4].__str__() + ":" + fecha[5].__str__()
        fech2 = datetime.datetime.strptime(fech, "%Y-%m-%d-%H:%M:%S")
        lastDateStr = lastDate.__str__()[0:19]
        lastDate2 = datetime.datetime.strptime(lastDateStr.__str__(), "%Y-%m-%d %H:%M:%S")

        if fech2 > lastDate2:
            noticia = Noticia(id_noticia=id, titulo=tit, descripcion=desc, url_foto=foto,url_noticia=url_not, fecha=fech2, procedente_de=revista, deporte=_deporte)
            noticia.save()

            for t in entrada.tags:
                try:
                    etiquetas = Etiquetas.objects.all()
                    if t['term'] in Etiquetas.objects.values_list('nombre', flat=True):
                        etiqueta = Etiquetas.objects.get(nombre=t['term'])
                        etiqueta.noticias.add(noticia)
                    else:
                        id = len(Etiquetas.objects.all())
                        name = t['term']
                        etiqueta = Etiquetas(id_etiqueta=id, nombre=name)
                        etiqueta.save()
                        etiqueta.noticias.add(noticia)
                except:
                    print ""


#EXTRACCIÓN DE DATOS DE AS - FUTBOL
@commit_on_success
def read_primera_division_AS():
    print "Populando FUTBOL de AS..."
    parseo = feedparser.parse('http://futbol.as.com/rss/futbol/primera.xml')

    #Tenemos que encontrar el ultimo id registrado
    if len(Noticia.objects.all()) == 0:
        counter = 1
        lastDate = datetime.datetime.today()
        lastDate = lastDate.replace(year=lastDate.year-3)
    else:
        if "AS-FUTBOL" not in Noticia.objects.values_list('procedente_de', flat=True):
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter += 1
            lastDate = datetime.datetime.today()
            lastDate = lastDate.replace(year=lastDate.year - 3)

        else:
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter+=1
            queryset = Noticia.objects.filter(procedente_de='AS-FUTBOL')
            lastDate = queryset.latest("fecha").fecha
            lastDate = lastDate.replace(hour=lastDate.hour + 1)

    for entrada in parseo.entries:
        _deporte = "FUTBOL"
        revista = "AS-FUTBOL"
        id = counter
        counter+=1
        tit = entrada.title
        desc = entrada.content[0]['value']
        desc = strip_tags(desc)
        desc = desc[0:150]
        url_not = entrada.link
        foto = entrada.links[1]['href']

        fecha = entrada.published_parsed
        fech = fecha[0].__str__() + "-" + fecha[1].__str__() + "-" + fecha[2].__str__() + "-" + (fecha[3]).__str__() + ":" + fecha[4].__str__() + ":" + fecha[5].__str__()
        fech2 = datetime.datetime.strptime(fech, "%Y-%m-%d-%H:%M:%S")
        lastDateStr = lastDate.__str__()[0:19]
        lastDate2 = datetime.datetime.strptime(lastDateStr.__str__(), "%Y-%m-%d %H:%M:%S")


        if fech2 > lastDate2:
            noticia = Noticia(id_noticia=id, titulo = tit, descripcion = desc, url_foto = foto, url_noticia = url_not, fecha = fech2, procedente_de=revista, deporte=_deporte)
            noticia.save()

            for t in entrada.tags:
                try:
                    if t['term'] in Etiquetas.objects.values_list('nombre', flat=True):
                        etiqueta = Etiquetas.objects.get(nombre=t['term'])
                        etiqueta.noticias.add(noticia)
                    else:
                        id = len(Etiquetas.objects.all())
                        name = t['term']
                        etiqueta = Etiquetas(id_etiqueta=id, nombre=name)
                        etiqueta.save()
                        etiqueta.noticias.add(noticia)
                except:
                    print ""






# Indexación de resultados

dirindexnoticias = "IndexNoticias"

def indexar_datos():

    print("Indexando Noticias...")

    # Creamos indice de Noticias
    if not os.path.exists(dirindexnoticias):
        os.mkdir(dirindexnoticias)

    ix_noticias = create_in(dirindexnoticias, schema=get_schema_noticias())
    writer_noticias = ix_noticias.writer()

    conn = sqlite3.connect('diariosDeportivos.db')
    cursor = conn.execute("""SELECT * FROM diarios_app_noticia""");
    for row in cursor:
        fecha = row[5]
        fecha2 = fecha.__str__()
        fecha3 = fecha2.split( )[0]
        writer_noticias.add_document(id_noticia=unicode(row[0]), titulo=unicode(row[1]), descripcion=unicode(row[2]), url_foto=unicode(row[3]),
                                     url_noticia=unicode(row[4]), fecha=unicode(fecha3), procedente_de=unicode(row[6]))
    conn.close()
    writer_noticias.commit()


def get_schema_noticias():
    return Schema(id_noticia=NUMERIC(stored=True), titulo=TEXT(stored=True), descripcion=TEXT(stored=True),
                  url_foto=ID(stored=True), url_noticia=ID(stored=True), fecha=DATETIME(stored=True),
                  procedente_de=KEYWORD(stored=True))


#EXTRACCIÓN DE DATOS DE EL MUNDO - FUTBOL
@commit_on_success
def read_primera_division_EL_MUNDO():
    print "Populando FUTBOL de EL MUNDO..."
    parseo = feedparser.parse('http://estaticos.elmundo.es/elmundodeporte/rss/futbol.xml')

    #Tenemos que encontrar el ultimo id registrado
    if len(Noticia.objects.all()) == 0:
        counter = 1
        lastDate = datetime.datetime.today()
        lastDate = lastDate.replace(year=lastDate.year-3)
    else:
        if "EL MUNDO-FUTBOL" not in Noticia.objects.values_list('procedente_de', flat=True):
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter += 1
            lastDate = datetime.datetime.today()
            lastDate = lastDate.replace(year=lastDate.year - 3)

        else:
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter+=1
            queryset = Noticia.objects.filter(procedente_de='EL MUNDO-FUTBOL')
            lastDate = queryset.latest("fecha").fecha
            lastDate = lastDate.replace(hour=lastDate.hour + 1)

    for entrada in parseo.entries:
        _deporte = "FUTBOL"
        revista = "EL MUNDO-FUTBOL"
        id = counter
        counter+=1
        tit = entrada.title
        desc = entrada.content[0]['value']
        desc = strip_tags(desc)
        desc = desc[0:150]
        url_not = entrada.link
        foto = entrada.media_content[0]['url']

        fecha = entrada.published_parsed
        fech = fecha[0].__str__() + "-" + fecha[1].__str__() + "-" + fecha[2].__str__() + "-" + (fecha[3]).__str__() + ":" + fecha[4].__str__() + ":" + fecha[5].__str__()
        fech2 = datetime.datetime.strptime(fech, "%Y-%m-%d-%H:%M:%S")
        lastDateStr = lastDate.__str__()[0:19]
        lastDate2 = datetime.datetime.strptime(lastDateStr.__str__(), "%Y-%m-%d %H:%M:%S")


        if fech2 > lastDate2:
            noticia = Noticia(id_noticia=id, titulo = tit, descripcion = desc, url_foto = foto, url_noticia = url_not, fecha = fech2, procedente_de=revista, deporte=_deporte)
            noticia.save()

            for t in entrada.tags:
                try:
                    if t['term'] in Etiquetas.objects.values_list('nombre', flat=True):
                        etiqueta = Etiquetas.objects.get(nombre=t['term'])
                        etiqueta.noticias.add(noticia)
                    else:
                        id = len(Etiquetas.objects.all())
                        name = t['term']
                        etiqueta = Etiquetas(id_etiqueta=id, nombre=name)
                        etiqueta.save()
                        etiqueta.noticias.add(noticia)
                except:
                    print ""



#EXTRACCIÓN DE DATOS DE AS - BASKET
@commit_on_success
def read_liga_endesa_AS():
    print "Populando BASKET de AS..."
    parseo = feedparser.parse('http://baloncesto.as.com/rss/baloncesto/acb.xml')

    #Tenemos que encontrar el ultimo id registrado
    if len(Noticia.objects.all()) == 0:
        counter = 1
        lastDate = datetime.datetime.today()
        lastDate = lastDate.replace(year=lastDate.year-3)
    else:
        if "AS-BASKET" not in Noticia.objects.values_list('procedente_de', flat=True):
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter += 1
            lastDate = datetime.datetime.today()
            lastDate = lastDate.replace(year=lastDate.year - 3)

        else:
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter+=1
            queryset = Noticia.objects.filter(procedente_de='AS-BASKET')
            lastDate = queryset.latest("fecha").fecha
            lastDate = lastDate.replace(hour=lastDate.hour + 1)

    for entrada in parseo.entries:
        _deporte = "BASKET"
        revista = "AS-BASKET"
        id = counter
        counter+=1
        tit = entrada.title
        desc = entrada.content[0]['value']
        desc = strip_tags(desc)
        desc = desc[0:150]
        url_not = entrada.link
        foto = entrada.links[1]['href']

        fecha = entrada.published_parsed
        fech = fecha[0].__str__() + "-" + fecha[1].__str__() + "-" + fecha[2].__str__() + "-" + (fecha[3]).__str__() + ":" + fecha[4].__str__() + ":" + fecha[5].__str__()
        fech2 = datetime.datetime.strptime(fech, "%Y-%m-%d-%H:%M:%S")
        lastDateStr = lastDate.__str__()[0:19]
        lastDate2 = datetime.datetime.strptime(lastDateStr.__str__(), "%Y-%m-%d %H:%M:%S")


        if fech2 > lastDate2:
            noticia = Noticia(id_noticia=id, titulo = tit, descripcion = desc, url_foto = foto, url_noticia = url_not, fecha = fech2, procedente_de=revista, deporte=_deporte)
            noticia.save()

            for t in entrada.tags:
                try:
                    if t['term'] in Etiquetas.objects.values_list('nombre', flat=True):
                        etiqueta = Etiquetas.objects.get(nombre=t['term'])
                        etiqueta.noticias.add(noticia)
                    else:
                        id = len(Etiquetas.objects.all())
                        name = t['term']
                        etiqueta = Etiquetas(id_etiqueta=id, nombre=name)
                        etiqueta.save()
                        etiqueta.noticias.add(noticia)
                except:
                    print ""


#EXTRACCIÓN DE DATOS DE EL MUNDO - BASKET
@commit_on_success
def read_liga_endesa_EL_MUNDO():
    print "Populando BASKET de EL MUNDO..."
    parseo = feedparser.parse('http://estaticos.elmundo.es/elmundodeporte/rss/baloncesto.xml')

    #Tenemos que encontrar el ultimo id registrado
    if len(Noticia.objects.all()) == 0:
        counter = 1
        lastDate = datetime.datetime.today()
        lastDate = lastDate.replace(year=lastDate.year-3)
    else:
        if "EL MUNDO-BASKET" not in Noticia.objects.values_list('procedente_de', flat=True):
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter += 1
            lastDate = datetime.datetime.today()
            lastDate = lastDate.replace(year=lastDate.year - 3)

        else:
            counter = Noticia.objects.latest("id_noticia").id_noticia
            counter+=1
            queryset = Noticia.objects.filter(procedente_de='EL MUNDO-BASKET')
            lastDate = queryset.latest("fecha").fecha
            lastDate = lastDate.replace(hour=lastDate.hour + 1)

    for entrada in parseo.entries:
        _deporte = "BASKET"
        revista = "EL MUNDO-BASKET"
        id = counter
        counter+=1
        tit = entrada.title
        desc = entrada.content[0]['value']
        desc = strip_tags(desc)
        desc = desc[0:150]
        url_not = entrada.link
        foto = entrada.media_content[0]['url']

        fecha = entrada.published_parsed
        fech = fecha[0].__str__() + "-" + fecha[1].__str__() + "-" + fecha[2].__str__() + "-" + (fecha[3]).__str__() + ":" + fecha[4].__str__() + ":" + fecha[5].__str__()
        fech2 = datetime.datetime.strptime(fech, "%Y-%m-%d-%H:%M:%S")
        lastDateStr = lastDate.__str__()[0:19]
        lastDate2 = datetime.datetime.strptime(lastDateStr.__str__(), "%Y-%m-%d %H:%M:%S")


        if fech2 > lastDate2:
            noticia = Noticia(id_noticia=id, titulo = tit, descripcion = desc, url_foto = foto, url_noticia = url_not, fecha = fech2, procedente_de=revista, deporte=_deporte)
            noticia.save()

            for t in entrada.tags:
                try:
                    if t['term'] in Etiquetas.objects.values_list('nombre', flat=True):
                        etiqueta = Etiquetas.objects.get(nombre=t['term'])
                        etiqueta.noticias.add(noticia)
                    else:
                        id = len(Etiquetas.objects.all())
                        name = t['term']
                        etiqueta = Etiquetas(id_etiqueta=id, nombre=name)
                        etiqueta.save()
                        etiqueta.noticias.add(noticia)
                except:
                    print ""


def prueba():

    news = Noticia.objects.all().order_by("-fecha")

    for n in news:
        print n.fecha



if __name__ == "__main__":
    read_primera_division_MARCA()
    read_liga_endesa_MARCA()
    read_primera_division_AS()
    read_liga_endesa_AS()
    read_primera_division_EL_MUNDO()
    read_liga_endesa_EL_MUNDO()
    indexar_datos()

    #prueba()