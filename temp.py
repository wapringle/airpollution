from browser import document, html, window, alert, timer, ajax
from wordsquare import *

import pprint


class x2():
    def __init__(self,id):
        self.id=id
    pass
class x1():
    def __init__(self,id):
        self.currentTarget=x2(id)
        
def null():
    pass

frontPage=null
showPuzzle()

ev=x1("i0101")
on_mouse_enter(ev)
on_grid_button_pressed(ev)
