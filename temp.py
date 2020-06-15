from browser import document, html, window, alert, timer, ajax

import pprint

#import bib
import json
"""
with open("img/bib.jsonld", 'r') as stream:
    try:
        config=(json.load(stream))
    except json.JSONDecodeError as exc:
        print(exc)


bib.loadConfig(config["pic3"])
#bib.frontPage(config)

def xx(**kwargs):
    print(picture)
    
bib.displayPic( {
    "picture": "img/traffic.png", 
    "startX": 100,
    "startY": 200,
    "width": 680,
    "height": 500,
    "highlights": [
      "427 100 590 200 This is a factory", 
      "345 231 426 300 This is a tractor", 
      "467 267 666 380 This is a bus", 
      "275 340 451 436 This is a lorry", 
      "71 336 221 436 This is a car", 
      "0 200 162 336 This is a house", 
      "104 116 269 210 These are trees", 
      "8 16 103 86 This is an aircraft"
    ]
  })    
    
"""

config=[]
with open("config/bib.jsonld", 'r') as stream:
    try:
        config=json.load(stream)
    except json.JSONDecodeError as exc:
        print(exc)

pprint.pprint(config[0])
import bib, bib2
bib.displayPic(document,config[0])
