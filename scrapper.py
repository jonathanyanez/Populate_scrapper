#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
import os
import time
import requests
import urllib.request
import logging
from bs4 import BeautifulSoup

#crear archivos de log
logging.basicConfig(filename='scrapper.log',level=logging.INFO)
#informacion de log
logging.info("[+] USER:"+os.environ ['HOME']+' '+'DATETIME:'+time.strftime("%x")+' '+time.strftime("%X"))

if len(sys.argv) ==2:
    directorio = sys.argv[1]
elif len(sys.argv)==1:
    directorio = "./"
else:
    print("Numero de argumentos invalido\n")
    sys.exit(1)



#direccion url solicitada en el ejercicio
url='http://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST8/EST10/EST305/1836?changeLanguage=es'


response=requests.get(url)


soup = BeautifulSoup (response.text, "html.parser")

#direccionweb
pattern_web="http://www.seg-social.es"
#patron de comienzo
pattern_begin_link="/wps/wcm/connect/wss/"
#patron de fin
pattern_end_link='CVID='


for link in soup.find_all('a'):
    href_link=link.get('href')

    #comprobamos que ese enlace tiene un href
    if href_link != None:
        if href_link.startswith(pattern_begin_link):
            if href_link.endswith(pattern_end_link):
                
                """
                A partir de aqui, se realiza el codigo para descargas
                """
                urldownlowad=pattern_web+href_link
                
                #deducir nuevo nombre
                index=urldownlowad.index("AfiliadosMuni-")+len("AfiliadosMuni-")
                download_name=urldownlowad[index+3:index+7]+urldownlowad[index:index+2]+".xlsx"
                print("archivo descargado: "+download_name)
                #descargar archivo y renombrar
                archivo_tmp, header=urllib.request.urlretrieve(urldownlowad)
                with open (directorio+download_name, 'wb') as archivo:
                    with open(archivo_tmp, 'rb') as tmp:
                        archivo.write(tmp.read())

#el programa se ejecuta sin problema
sys.exit(0)
            


