from browser import document, html, window, alert, timer, ajax
from  browser.html import *
import json


"""
Script to create a canvas, load a picture and create a number of hightlight areas that produce a popup on mouseover.

The highlight areas are rectangles that invisibly overlay the image. When the mouse enters the highlight area
a popup appears over the area. The coordinates in he table below give the 
top left and bottom right of the overlay, relative to the coordinates of the underlying image. These are
converted to absolute coordinates by adding the XY coordinates of the image.

The mouse coordinates are displayed in the table for diagnostic purposes.

"""

dbg=True
pageIndex=0
jsonConfig=[]
def read(f):
    global pageIndex,jsonConfig
    jsonConfig=json.loads(f.read())
    print('loaded')
    displayPic(document['action'],jsonConfig[pageIndex])

def loadConfig():
    print("loading")
    req = ajax.get("config/bib.jsonld", mode="text", oncomplete=read)

def fastConfig():
    global pageIndex,jsonConfig
    jsonConfig.append(
        {'filename': '1-BiB-Slide.png',
         'highlights': [{'brx_pc': '9',
                         'bry_pc': '33',
                         'star': '1',
                         'text': 'The atmosphere acts like a jacket to keep the planet '
                                 'warm.  If there was no atmosphere the Earth would be '
                                 'about -18 C. Brr',
                         'tlx_pc': '2',
                         'tly_pc': '20'},
                        {'brx_pc': '48',
                         'bry_pc': '85',
                         'star': '2',
                         'text': 'If the earth was the size on an apple, the '
                                 'atmosphere would be thinner than the skin of the '
                                 'apple.',
                         'tlx_pc': '42',
                         'tly_pc': '72'}],
         'ratio': '2.6'}
)
    displayPic(document['action'],jsonConfig[pageIndex])
    
    
def update_checkboxes(ev):
    # updates checkboxes when the selection has changed
    #selected = [option.value for option in sel if option.selected]
    pass
    

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
    
            


class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)
        self.width=int(window.innerWidth * 7 /8)
        print(f'width {self.width}')
        self.height=int(self.width/float(self.ratio))
        self.picture='img/'+self.filename

def cv(a,b):
    a=0 if a=='' else int(a)
    return int(a*b/100 +0.5)

def vc(a,b):
    return int(a*100/b +0.5)
    

class Highlight(object):
    def __init__(self, adict,q):
        
        self.__dict__.update(adict)
        self.tlx = cv(self.tlx_pc,q.width)
        self.tly = cv(self.tly_pc,q.height)
        self.brx = cv(self.brx_pc,q.width)
        self.bry = cv(self.bry_pc,q.height)
        

def displayPic(doc,config):
    def px(x):
        return str(x)+"px"
    q=Bunch(config)
    canvas = CANVAS(id="canvas",width =q.width, height = q.height)
    #canvas.style={"position": "absolute", "left": px(q.startX), "top": px(q.startY) }    
    canvas.bind("mousemove", mousemove)
    
    doc <= canvas # this brython operator writes the canvas to the base document

    q.startX=canvas.offsetLeft
    q.startY=canvas.offsetTop
    print(f"canvas {q.startX} {q.startY} ")
    
    """ Cant work out how to load image into canvas with brython so drop into javascript here   """

    window.loadImage(canvas,q.picture,q.width,q.height) # keep these same as canvas dimensions
    
    i=0
    for temp in q.highlights:
        h=Highlight(temp,q)

        """
        t2=temp.split(" ",4)
        tlx, tly, brx, bry = map(int,t2[:4])
        text=t2[-1]
        """
        
        """ Create the individual highlight areas """

        highlight_id=f'V{i}'
        c2 = CANVAS(id=highlight_id, width=h.brx - h.tlx ,height=h.bry - h.tly )
        c2.style={"position": "absolute", "left": px(h.tlx+q.startX), "top": px(h.tly+q.startY) }
        ct2 = canvas.getContext('2d')
        """ Bind the mouse events to the individual highlight areas """
        
        """
        ct2.rect(h.tlx+q.startX, h.tly+q.startY, h.brx - h.tlx, h.brx - h.tlx)
        grd = ct2.createRadialGradient(150, 150, 10, 150, 150, 150)
        grd.addColorStop(0, '#8ED6FF')
        grd.addColorStop(1, '#004CB3')
        ct2.fillStyle = grd
        ct2.fill()
        print("filled")
        """
        
        
        c2.bind('mouseenter', mouseenter)
        c2.bind('mouseleave', mouseout)

        doc <= c2

        
        popup_id="popup"+highlight_id
        txt=SPAN(h.text,id=popup_id, Class="tooltiptext")

        tooltip=DIV(txt )
        tooltip.style={
            "position": "absolute", 
            "left": px((h.tlx+h.brx)/2+q.startX), 
            "top": px((h.tly+h.bry)/2+q.startY),
            "zIndex": 1,
            'visibility': 'hidden' 
        }
        
        
        txt.bind('mouseleave', mouseout)
        doc <= tooltip

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
    document["popup"+ev.currentTarget.id].style['visibility']='visible' # turn popup on 

def mouseleave(ev):
    if dbg: document["trace1"].text = f'leaving {ev.currentTarget.id}'
    document["popup"+ev.currentTarget.id].style['visibility']='hidden' # turn popup off
    
def mouseout(ev):
    global cvs
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

    #document["trace3"].text = f"coordinates : {X}, {Y}"
    #document["trace1"].text = f'leaving {ev.currentTarget.id}  {X}, {Y} { X - box.offsetLeft} {Y - box.offsetTop} '
    if  0 <= X - box.offsetLeft  <= box.width \
    and 0 <= Y - box.offsetTop   <= box.height :    
        return
    document[popup_id].style['visibility']='hidden' # turn popup off
    

