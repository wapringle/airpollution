from browser import document, html, window, alert, timer
from  browser.html import *
import bibconfig

""" dummy chnage """
"""
Script to create a canvas, load a picture and create a number of hightlight areas that produce a popup on mouseover.

The highlight areas are rectangles that invisibly overlay the image. When the mouse enters the highlight area and is clicked
a popup appears over the area. The coordinates in he table below give the 
top left and bottom right of the overlay, relative to the coordinates of the underlying image. These are
converted to absolute coordinates by adding the XY coordinates of the image.

The mouse coordinates are displayed in the table for diagnostic purposes.

"""
 
dbg=False
clickModel=True

pageIndex=0
jsonConfig=[]

def load():
    """ Config is stored as python structure in bibconfig.py """
    global pageIndex,jsonConfig
    jsonConfig=bibconfig.config

def frontPage():
    
    def shift_left(ev):
        global pageIndex,jsonConfig
        if pageIndex > 0:
            pageIndex -= 1
        
        main.clear()
        
        displayPic(main,jsonConfig[pageIndex])
    
    def shift_right(ev):
        global pageIndex,jsonConfig
        if pageIndex < len(jsonConfig) -1:
            pageIndex += 1
        
        main.clear()
        
        displayPic(main,jsonConfig[pageIndex])

    """ Elements are laid out using the grid css model. Could replace with a table """

    document <= DIV(
        DIV( Class="item6",id="Left2")+
        DIV( Class="item1",id="Header")+
        DIV( Class="item7",id="Right2")+
        DIV( Class="item3",id="Main")+
        DIV( Class="item5",id="Footer", style={  "font-family": "Arial, Helvetica, sans-serif;"}),
        
        Class="grid-container"
    )
    header = document["Header"]
    header <= H1(SPAN("Ho Ho Ho",Class='hhh'))
    
    l=BUTTON(SPAN("<"),Class="dir")
    document["Left2"] <= l
    #l.bind("click",shift_left)
    l.bind("mousedown",shift_left)
    
    r = BUTTON(SPAN(">"),Class="dir")
    document["Right2"] <= r
    #r.bind("click",shift_right)
    r.bind("mousedown",shift_right)
    
    main= DIV(id="action",style={"width": "100%", "height": "80%"})
    document["Main"] <= main

    displayPic(main,jsonConfig[pageIndex])
    

class Bunch(object):
    """ Save the lines from slides.cvs file as attributes. Easier to handle """
    def __init__(self, adict):
        self.__dict__.update(adict)
        self.width=int(window.innerWidth) - 20 # * 7 /8)
        self.height=int(self.width/float(self.ratio))
        self.picture='img/'+self.filename

def cv(a,b):
    """ Convert percentage to absolute """
    a=0 if a=='' else int(a)
    return int(a*b/100 +0.5)

def vc(a,b):
    """ and vice versa """
    return int(a*100/b +0.5)
    

class Highlight(object):
    """ Ditto for Popup_Summary.csv, coverting percentages to absolute """
    def __init__(self, adict,q):
        
        self.__dict__.update(adict)
        self.tlx = cv(self.tlx_pc,q.width)
        self.tly = cv(self.tly_pc,q.height)
        self.brx = cv(self.brx_pc,q.width)
        self.bry = cv(self.bry_pc,q.height)
        

def px(x):
    return str(x)+"px"

def displayPic(doc,config):
    
    """ Display apicure using data from config """
    
    q=Bunch(config)
    q.width=doc.offsetWidth-40 # make it as fullscreen as possible, allow for margins
    q.height=int(q.width/float(q.ratio))
    canvas = CANVAS(id="canvas",width =q.width, height = q.height)
    canvas.bind("mousemove", mousemove)
    
    doc <= canvas # this brython operator writes the canvas to the base document

    q.startX=canvas.offsetLeft
    q.startY=canvas.offsetTop
    
    """ Cant work out how to load image into canvas with brython so drop into javascript here   
    #window.loadImage(canvas,q.picture,q.width,q.height) # keep these same as canvas dimensions

    Finally worked it out. Simple if you know how
    
    """

    ctx = canvas.getContext('2d')

    v = IMG(src=q.picture,id='pic') 
    v.onload=lambda ev: ctx.drawImage(v,0,0,q.width,q.height)

    i=0
    for temp in q.highlights:
        if dbg:
            break
        h=Highlight(temp,q)
        
        """ Create the individual highlight areas """

        highlight_id=f'V{i}'
        c2 = CANVAS(id=highlight_id, width=h.brx - h.tlx ,height=h.bry - h.tly )
        
        c2.style={"position": "absolute", "left": px(h.tlx+q.startX), "top": px(h.tly+q.startY), "cursor": "pointer", "-webkit-touch-callout" : "none" }
        ct2 = canvas.getContext('2d')

        """ Bind the mouse events to the individual highlight areas """
        
        if clickModel:
            
            """ Click over area for popup """
            c2.bind('mousedown', mouseenter)
            c2.bind('mouseup', mouseleave)
            c2.bind('mouseleave', mouseout)
        else:
            
            """ Else mouseover """
            c2.bind('mouseenter', mouseenter)
            c2.bind('mouseleave', mouseout)

        doc <= c2

        """ This is the popup """
        
        popup_id="popup"+highlight_id
        txt=SPAN(h.text,id=popup_id, Class="tooltiptext")

        tooltip=DIV(txt )
        tooltip.style={
            "position": "absolute", 
            "left": px(min((h.tlx+h.brx)/2+q.startX, q.width - 500 )), #  if necessary, adjust lhs to stop popup overflowing page
            "top": px((h.tly+h.bry)/2+q.startY ),
            "zIndex": 1,
            'visibility': 'hidden' 
        }
        
        if clickModel:
            txt.bind('mouseup', mouseleave)
            txt.bind('mouseleave', mouseout)
        else:
            txt.bind('mouseleave', mouseout)
        doc <= tooltip
        pp=document[popup_id]
        pp.style['top']= px(pp.offsetTop - pp.offsetHeight - 50)

        i+=1
        
    """ Create a little table to display the mouse details.
        This is much more civilised than HTML or javascript.
    """
    table = TABLE()
    #table <= TR(TD( H1("Mouse over image demo"),colspan=2)) 
    if dbg: table <= TR(TD(DIV(id="trace3"))+TD(DIV(id="trace1")))
    
    """ Finally write the table to document """
    document["Footer"] <= table 
    
    return doc
    
""" mouse events """

def mousemove(ev):
    if dbg: document["trace3"].text = f"coordinates : {vc(ev.layerX,document['canvas'].offsetWidth)}, {vc(ev.layerY,document['canvas'].offsetHeight)}"
    pass


def mouseenter(ev):
    if dbg: document["trace1"].text = f'entering {ev.currentTarget.id}'
    pp= document["popup"+ev.currentTarget.id]
    pp.style['visibility']='visible' # turn popup on 
    ev.preventDefault()

def mouseleave(ev):
    if dbg: document["trace1"].text = f'leaving {ev.currentTarget.id}'

    id=ev.currentTarget.id
    if id[:5]=="popup":
        frame_id=id[5:] 
        popup_id=id
        box=document[frame_id]
    else:
        frame_id=id
        popup_id="popup"+id
        box=document[popup_id].parent
        box=document[frame_id]

    document[popup_id].style['visibility']='hidden' # turn popup off
    
def mouseout(ev):
    id=ev.currentTarget.id
    if id[:5]=="popup":
        frame_id=id[5:] 
        popup_id=id
        box=document[frame_id]
    else:
        frame_id=id
        popup_id="popup"+id
        box=document[popup_id].parent
        box=document[frame_id]
        
    X=ev.clientX
    Y=ev.clientY

    if dbg: document["trace1"].text = f'leaving {ev.currentTarget.id}  {X}, {Y} { X - box.offsetLeft} {Y - box.offsetTop} '
    
    """ Ignore if mouse still inside popup or star """
    
    if  0 <= X - box.offsetLeft  <= box.width \
    and 0 <= Y - box.offsetTop   <= box.height :    
        return
    
    """ else turn popup off """
    document[popup_id].style['visibility']='hidden' 
    
