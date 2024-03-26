#On récupère l'alerte cert la plus récente depuis https://www.cert.ssi.gouv.fr/alerte/feed/

import requests
import xml.etree.ElementTree
import datetime

#On récupère le contenu du premier span et on le met dans un array ou un dictionnaire pour le retourner
def get_cert_alert():
    url = "https://www.cert.ssi.gouv.fr/alerte/feed/"
    response = requests.get(url)
    
    #On parse le XML
    root = xml.etree.ElementTree.fromstring(response.content)
    items = root.findall("channel/item")

    temp = 0
    
    #On parcoure les items pour récupérer le contenu du plus récent
    for item in items:
        title = item.find("title").text
        #description = item.find("description").text
        link = item.find("link").text
        pubDate = item.find("pubDate").text

        #Conversion de la pubDate en timestamp
        timestamp = datetime.datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %z").timestamp()

        #On compare le timestamp actuel avec le timestamp de l'item actuel
        if temp < timestamp:
            temp = timestamp

            result = {
                "title": title,
                #"description": description,
                "link": link,
                "pubDate": pubDate,
            }

    return result