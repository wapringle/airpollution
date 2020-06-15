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

def read(f):
    global highlight
    jsonConfig=json.loads(f.read())
    frontPage(jsonConfig)

def loadConfig():
    print("loading")
    req = ajax.get("img/bib.jsonld", mode="text", oncomplete=read)



    
def update_checkboxes(ev):
    # updates checkboxes when the selection has changed
    #selected = [option.value for option in sel if option.selected]
    pass
    

def frontPage(config):
    global flag
    flag=False
    def show_selected(ev):
        global flag 
        index=[option.value for option in sel if option.selected]
        if len(index):
            if flag:
                del document["base"]
            pic=pictures[int(index[0])]
            #alert(pic)
            doc=displayPic(config[pic])
            document <= doc
            flag=True
            

    document <= H1("Ho Ho Ho")
    pictures=sorted(config.keys())
    sel = SELECT(OPTION(elt, value=i)
        for i, elt in enumerate(pictures))    
    
    sel.bind("change", update_checkboxes)
    b = BUTTON("Select")
    b.bind("click", show_selected)
    document <= sel + b

class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)
        self.width=int(window.innerWidth * 7 /8)
        print(f'width {self.width}')
        self.height=int(self.width/self.ratio)

def cv(a,b):
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
    

