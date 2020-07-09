from browser import document, html, alert
from browser.html import *


from WordSearch import WordSearch

def frontPage():

  def shift_left(ev):
    pass

  def shift_right(ev):
    pass

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
  header <= H1(SPAN("Word Search",Class='hhh'))

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




def tuple2id(t): return "i%02d%02d" % t

def id2tuple(id): return (int(id[1]),int(id[2]))

def makeWordSearch():
  # words = a variable with all the words, which are all separated by a comma.
  # Note : the variable which contains all words mustn't be called words.
  words = ("Hello,Blah,Superhero,XXXXX")
  x = 10
  y = 10
  # x & y indicate the size of the word search.
  # Note: When you take a look at our code, you will see 'grid' (a list).
  #Grid is a a list which contains lists(columns) which contain letters (strings). 
  w = WordSearch(words,x,y)
  #for i in w.grid:
  #  print(" ".join(i))


def set_backGround(id,cell):
  document[id].style.backgroundColor=cell.status.background

class State():
  def is_clicked(self): return False
  def name(self): 
    return self.__class__.__name__
  def mousein(self):
    return None
  def mouseout(self):
    return None
  def click(self):
    return None

class unused(State):
  background='ivory'

  def mousein(self):
    return highlight()

class highlight(State):
  background='#eefbff'

  def click(self):
    return clicked()
  def mouseout(self):
    return unused()

class clicked(State):
  background='#f33fba4d'

  def is_clicked(self): return True
  def click(self):
    return highlight()
  def mousein(self):
    return clicked()
  def mouseout(self):
    return clicked()

class GridSquare():
  def __init__(self,id):
    self.id=id
    self.status=unused()
  def action(self,act):
    self.status=getattr(self.status,act)()

def initCell(row,column):
  global gridDict
  id=tuple2id((row,column))
  gridDict[id]=GridSquare(id)
  return id

def on_mouse_enter(ev): 
  #document["progress"].text=f'entering {ev.currentTarget.id} {gridDict[ev.currentTarget.id].status.name()}'
  global gridDict
  itm=ev.currentTarget
  id=itm.id
  cell=gridDict[id]
  cell.action("mousein")
  set_backGround(id, cell)

def on_mouse_leave(ev): 
  itm=ev.currentTarget
  id=itm.id
  cell=gridDict[id]
  cell.action("mouseout")
  set_backGround(id, cell)
    #document[id].style.backgroundColor=cell.status.background()
    
def on_grid_button_pressed(ev): 
  itm=ev.currentTarget
  id=itm.id

  cell=gridDict[id]
  cell.action("click")
  set_backGround(id, cell)
  
  found=[ k for k,v in gridDict.items() if v.status.is_clicked() ]
  print(found)
  print(activeSquares)
  if set(found) == activeSquares:
    alert("Contratulations! You found all the words")
    


def make_grid(w,grid_size):
  
  t = html.TABLE(Class="ws")
  tb = html.TBODY()
  t <= tb
  for row in range(grid_size):
    wordline=w.grid[row]
    line = html.TR()
    tb <= line
    for column in range(grid_size):
      val=wordline[column]
      id = initCell(row + 1, column + 1)
      cell = html.TD(val, id=id, Class="ws")
      line <= cell

      cell.bind("mouseenter", on_mouse_enter)
      cell.bind("mouseleave", on_mouse_leave)
      cell.bind("click", on_grid_button_pressed)
      cell.style.contentEditable = True
      

  return t

def showPuzzle():
  global gridDict, activeSquares
  grid_size=15
  words = ("OXYGEN,PARTICULATES,POLLUTION,NITROGEN")
  #words=("ZZZZZZ")
  w =WordSearch(words,grid_size,grid_size)
  
  gridDict={}
  activeSquares=set( [ tuple2id((r+1,c+1)) for r in range(grid_size) for c in range(grid_size) if w.nakedSquare[r][c] != '*'])
  wordList=list(map(LI,words.split(",")))
  for p in wordList:
    p.style={"text-align": "left"}
  waffle = DIV(
    SPAN("Can you find these words in the box?")+
    UL(
      wordList
    )+
    SPAN("Click on the words you find")
  )    
  return  html.TABLE(TR(TD(DIV(make_grid(w,grid_size),xClass="border")) + TD(waffle)),style={"backgroundColor": "#99f9ea", "margin": "auto"})

def load():
  frontPage()
  document["action"] <= showPuzzle()