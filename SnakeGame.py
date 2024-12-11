import random
import curses

s = curses.initdcr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

snk_x = sw/4
snk_y = sh/2
snake = [ 
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2],
]

food = [sh/2, sw/2]
w.adddch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT

while True:
    next_key