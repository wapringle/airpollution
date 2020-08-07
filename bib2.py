from browser import document, html, window, alert, timer, ajax
from  browser.html import *

import bib

def px(x):
    return str(x)+"px"

pic1={
    "picture": "img/1-BiB-Slide.png", 
    "ratio": 2.6,
    "highlights": [ {
        "tlx_pc": 1,
        "tly_pc": 19,
        "brx_pc": 9,
        "bry_pc": 35,
        "text": "The atmosphere acts like a jacket to keep the planet warm.  If there was no atmosphere the Earth would be about -18 C. Brr", 
         }, {
        "tlx_pc": 41,
        "tly_pc": 70,
        "brx_pc": 49,
        "bry_pc": 85,
        "text": "If the earth was the size on an apple, the atmosphere would be thinner than the skin of the apple."
      }
    ]
  }
pic2={
    "picture": "img/2-BiB-Slide.png", 
    "ratio": 2.6,
    "highlights": [ {
        "tlx_pc": 49,
        "tly_pc": 75,
        "brx_pc": 56,
        "bry_pc": 88,
        "text": "The atmosphere acts like a jacket to keep the planet warm.  If there was no atmosphere the Earth would be about -18 C. Brr", 
        }, {
        "tlx_pc": 86,
        "tly_pc": 75,
        "brx_pc": 92,
        "bry_pc": 91,
        "text": "If the earth was the size on an apple, the atmosphere would be thinner than the skin of the apple."
        }
    ]
  }

def frontPage():
    
    def shift_left(ev):
        main.clear()
        doc = bib.displayPic(main,pic2)
    
    def shift_right(ev):
        main.clear()
        bib.displayPic(main,pic2)
    
    document <= DIV(
        DIV( Class="item1",id="Header")+
        DIV( Class="item2",id="Left1")+
        DIV( Class="item2a",id="Left2")+
        DIV( Class="item2b",id="Left3")+
        DIV( Class="item3",id="Main")+  
        DIV( Class="item4",id="Right1")+
        DIV( Class="item4a",id="Right2")+
        DIV( Class="item4b",id="Right3")+
        DIV( Class="item5",id="Footer"),
        Class="grid-container"
    )
    header = document["Header"]
    header <= H1(SPAN("Ho Ho Ho"))
    l=BUTTON(SPAN("<"),Class="dir")
    document["Left2"] <= l
    l.bind("click",shift_left)
    r = BUTTON(SPAN(">"),Class="dir")
    document["Right2"] <= r
    r.bind("click",shift_right)
    main= DIV(id="action",style={"width": "100%", "height": "80%"})
    document["Main"] <= main
    
    bib.displayPic(main,pic1)
    
