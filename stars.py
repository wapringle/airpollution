from browser import document, html, window, alert, timer
from  browser.html import *
import math
import operator    
class Point():
    def __init__(self, *args):
        if isinstance(args[0],tuple):
            self.val=args[0]
        else:
            self.val=tuple(args)
    def __str__(self):
        return 'Point({self[0]:> 8.2f}, {self[1]:> 8.2f})'.format(self=self)

    def __getitem__(self,i):
        return self.val[i]
    
    def op(self,f,q):
        if isinstance(q,Point):
            return Point(*[ f(self[i],q[i]) for i in range(len(self.val))])
        else:
            return Point(*[ f(self[i],q)    for i in range(len(self.val))])
        
    def __add__(self, q):
        return self.op(operator.__add__,q)
    
    def __sub__(self,q):
        return self.op(operator.__sub__,q)
        
    def __mul__(self, q):
        return self.op(operator.__mul__,q)
    
    def __truediv__(self,q):
        return self.op(operator.__truediv__,q)

            
    def __iadd__(self, q):
        self.val=self.__add__(q).val
        return self
            
    def __isub__(self, q):
        self.val=self.__sub__(q).val
        return self
            
    def __imul__(self, q):
        self.val=self.__mul__(q).val
        return self
    
    def distanceTo(self,p):
        """ return distance between 2 points """
        r=self - p
        return math.sqrt(r[0]**2 + r[1]**2)
    
    def rotate(self,origin, angle):
        """ rotate point round origin by angle """
        s2= self -origin
        s3=s2 * math.cos(angle)
        s4=s2 * math.sin(angle)
    
        return Point(s3[0]-s4[1],s3[1]+s4[0]) + origin

    """
    def __idiv__(self, q):
        self.val=self.__div__(q).val
        return self
        """            

    
class Bunch(object):
    """ Save the lines from slides.cvs file as attributes. Easier to handle """
    def __init__(self, adict):
        self.__dict__.update(adict)
        self.width=int(window.innerWidth) - 20 # * 7 /8)
        self.height=int(self.width/float(self.ratio))
        self.picture='img/'+self.filename
        

star=[
    Point(-100.00,0.00),
    Point(-130.90,95.11),
    Point(-161.80,0.00),
    Point(-261.80,0.00),
    Point(-180.90,-58.78),
    Point(-211.80,-153.88),
    Point(-130.90,-95.11),
    Point(-50.00,-153.88),
    Point(-80.90,-58.78),
    Point(0.00,-0.00),
]
centre=Point(131,42.5)
def plus(s,offset,scale):
    return s * scale + offset 


def makeShape(ctx,pList,offset=0,scale=1):
    ctx.beginPath()
    nn=False
    for ss in pList:
        s2=plus(ss,offset,scale)
        if nn:
            ctx.moveTo(s2[0],s2[1])
            nn=False
        else:
            ctx.lineTo(s2[0],s2[1])
    ctx.closePath()

    ctx.fillStyle="yellow"
    ctx.lineWidth=4
    ctx.strokeStyle = "red";
    ctx.fill()
    ctx.stroke()
    

star2=[s+centre for s in star]

def makeStar(canvas):
    ctx = canvas.getContext('2d')
    ctx.fillStyle= "transparent"
    ctx.fillRect(0,0,canvas.width,canvas.height)
    #ctx.strokeRect(0,0,canvas.width,canvas.height)
    makeShape(ctx,star2,Point(canvas.width/2,canvas.height/2),1)
    
class Shape():
    def __init__(self,picture,size,XXX=Point(0,0),angle=0.0,scale=100,offset=Point(0,0)):
        """
        print(locals())
        self.__dict__.update(dict(locals()))
        print(self.XXX)
        del self.self
        """
        self.picture=picture
        self.size=size
        self.XXX=XXX
        self.angle=angle
        self.scale=scale
        self.offset=offset
        self.move=0
        self.alpha=1.0
        
    def draw(self,ctx):
        rotationPoint=self.XXX+self.offset
        ctx.translate(rotationPoint[0],rotationPoint[1])
        ctx.rotate(self.angle)
        ctx.globalAlpha=self.alpha
        ctx.drawImage(self.picture,-self.offset[0],-self.offset[1],self.size[0],self.size[1])
        ctx.rotate(-self.angle)
        ctx.translate(-rotationPoint[0],-rotationPoint[1])
        
    def update(self,timestamp):
        self.move=min( self.move+0,800)
        self.angle+=0.05
    
        
def XXonload():
    shapeList=[]
    def displayPic(timestamp):
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.strokeRect(0,0,canvas.width,canvas.height)
        ctx.fillStyle= "#99f9ea"
        ctx.fillRect(0,0,canvas.width,canvas.height)
        
        """ Draw canvas ct2 at position x,y with rotation "angle" """
        
        for s in shapeList:
            s.update(timestamp)
            s.draw(ctx)
    
    config={
    "ratio": 1.2,
    "filename": "1-BiB-Slide.png",
    }
    main= DIV(id="action",style={"width": "100%", "height": "80%"})

    document <= main
    ww=main.offsetWidth

    canvas = CANVAS(id="canvas" ,width = ww-40, height = ww * 2 /3.0 )
    ctx = canvas.getContext('2d')
    #ctx.globalCompositeOperation='source-out'
    main <= canvas

    c2=CANVAS(id="c2" ,width = 300, height = 300 )
    makeStar(c2)
    size=Point(c2.width,c2.height)
    
    shapeList.append(Shape(c2,size,Point(500,500),offset=Point(150,150)))
    shapeList.append(Shape(c2,size,Point(100,100),offset=Point(150,150)))
    #shapeList.append(Shape(c2,size,Point(600,600),offset=Point(150,150)))
    

    
    def drawFrame (timestamp):
        #window.requestAnimationFrame(drawFrame)
        displayPic(timestamp)
        
        
    drawFrame(0)


class Bunch(object):
    """ Save the lines from slides.cvs file as attributes. Easier to handle """
    def __init__(self, adict):
        self.__dict__.update(adict)
        self.width=int(window.innerWidth) - 20 # * 7 /8)
        self.height=int(self.width/float(self.ratio))
        self.picture='img/'+self.filename



class Background(Shape):
    def __init__(self,picture,id,size,start,duration,repeat,alpha):
        super().__init__(picture,size)
        self.id=id
        self.start=start
        self.duration=duration
        self.repeat=repeat
        self.state=0 # waiting for start
        self.stateChange=self.start
        self.aa=alpha
        self.alpha=1.0 if self.aa >0 else 0.0
        
    def update(self, timestamp):
        self.angle=0.0
        return
    def canDraw(self,elapsed):
        if self.duration < 0:
            return True
        if elapsed < self.start:
            return False
        elif self.state == 0:
            self.state=1
            self.stateChange=elapsed + self.duration
            return True
        elif self.state==1:
            if elapsed <  self.stateChange:
                self.alpha=(self.stateChange - elapsed) / self.duration
                if self.aa <0:
                    self.alpha=1-self.alpha
                return True
            else:
                self.state=2
                self.stateChange=elapsed + self.repeat
                return False
        elif self.state==2:
            if elapsed <  self.stateChange:
                return False
            else:
                self.state=1
                self.stateChange=elapsed + self.duration
                self.alpha=1.0 if self.aa >0 else 0.0
                return True
        else:
            print("ERROR")
            return False
        
    def nextActive(self,active):
        return self.stateChange
        
            
        
        

        
tsave=0.0
nxt=0
pic=0
        
def onload():
            
    config={
    "ratio": 2.6,
    "filename": "7-BiB-layer0.png",
    }
    
    q=Bunch(config)
    main= DIV(id="action",style={"width": "100%", "height": "80%"})

    document <= main
    q.width=main.offsetWidth-40

    canvas = CANVAS(id="canvas" ,width = q.width, height = q.height )
    main <= canvas
    
    animate(canvas)
    
def animate(canvas):
    global nxt,tsave
    ctx = canvas.getContext('2d')
    size=Point(canvas.width,canvas.height)

    frames=[
        Background('7-BiB-layer0.png','layer0',size,0.0,-1,0,1.0),
        Background('7-BiB-layer1.png','layer1',size,0.0,1000,1000,1.0),
        Background('7-BiB-layer3.png','layer3',size,3000,2000,4000,0.5),
        Background('7-BiB-layer4.png','layer4',size,3500,1500,4500,0.3),
        Background('7-BiB-layer5.png','layer5',size,4000,1000,5000,0.1),
        ]
    for f in frames:
        v = IMG(src='img/'+f.picture,id=f.id) 
        v.onload=lambda ev: ctx.drawImage(v,0,0,canvas.width,canvas.height)
        f.picture=v
        
    def displayPic2(elapsed):
        global nxt,pic
        if elapsed > nxt:
            for f in frames:
                if f.canDraw(elapsed):
                    f.draw(ctx)
            nxt = min(f.nextActive(elapsed) for f in frames)

    def drawFrame (timestamp):
        global  tsave,nxt
        if nxt< 200:
            window.requestAnimationFrame(drawFrame)
        if tsave==0.0:
            tsave=timestamp
        else:
            displayPic2(timestamp-tsave)#,v,ctx,frames,q)
        
    tsave=0.0
    nxt=0.0
    drawFrame(0)


#onload()
i=1