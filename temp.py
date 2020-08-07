from browser import document, html, window, alert, timer, ajax
from wordsquare import on_mouse_enter,on_grid_button_pressed,load
import wordsquare

import pprint
        
load()

ev=html._EV("i0101")
dd=html.DIV("hello",id="hello")
on_mouse_enter(ev)
on_grid_button_pressed(ev)
on_grid_button_pressed(ev)
global activeSquares
for id in wordsquare.activeSquares:
    ev=html._EV(id)
    on_mouse_enter(ev)
    on_grid_button_pressed(ev)
    
i=1