#! /usr/bin/python

import pyglet
from pyglet.media import procedural

seeds = [2,3] # Fibonacci starting point
size_threshold = 42
max_objects = 31 # max triangle on screen
timedelta = 0.13 # approximate time between two updates

# played_frequency = freq_offset +((freq_multip*F)%freq_modulo)
freq_offset = 200
freq_multip = 8
freq_modulo = 500
tunetime = 2*timedelta # length of one frequency

window = pyglet.window.Window(fullscreen=False,
                              style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)

triangle_list = [pyglet.graphics.vertex_list(3,('v2f',[0,0,0,0,0,0]),
                                             ('c3f',[0,0,0,0,0,0,0,0,0]))
                 ]

pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
player_list = []

def fibonagen(threshold=0):
    n0 = seeds[0]
    n1 = seeds[1]

    while True:
        yield n0
        n0 = n0+n1
        n1 = n0-n1 # no+n1-n1 = n0
        n0 = n0-n1 # no+n1-n0 = n1
        n1 = n0+n1 # there n0=n1, and n1=n0+n1

        if threshold:
            if n0>threshold:
                n0 = seeds[0]
                n1 = seeds[1]

def sidegen():
    x = 0
    while True:
        yield x
        x = (x+1)%4

fibonacci_color = fibonagen()
fibonacci_size = fibonagen(threshold=size_threshold)
sides = sidegen()

def limit_objects():

    global triangle_list, player_list

    # number of triangle
    triangle_list = triangle_list[-max_objects:]

    # number of sound player
    while len(player_list)>6:
        player_list[0].delete()
        player_list.pop(0)

def update(dt):
    
    size = window.get_size()
    
    cfibon = next(fibonacci_color)
    sfibon = next(fibonacci_size)
    side = next(sides)

    # one for each screen side, ugly but still
    positions = [(0,0,size[0],0,size[0],size[1]/sfibon),
                 (size[0],0,size[0],size[1],size[0]*(1.00-1.00/sfibon),size[1]),
                 (size[0],size[1],0,size[1],0,size[1]*(1.00-1.00/sfibon)),
                 (0,size[1],0,0,size[0]/sfibon,0)]
    
    rfib = (0.5+((cfibon%256)/256.00))%1.00
    gfib = 1.00-((cfibon%256)/256.00)
    bfib = (0.5-((cfibon%256)/256.00))%1.00
    
    colors = [rfib,gfib,bfib,rfib,gfib,bfib,rfib,gfib,bfib]
    vertices = positions[side]

    triangle = pyglet.graphics.vertex_list(3,('v2f',vertices),('c3f',colors))
    triangle_list.append(triangle)
    pyglet.gl.glClearColor(rfib,gfib,bfib,0.3)

    ffibon = freq_offset +((freq_multip*cfibon)%freq_modulo)
    p = procedural.Sine(tunetime,ffibon)
    player_list.append(p.play())
    
    limit_objects()

@window.event
def on_draw():
    window.clear()
    for triangle in triangle_list:
        triangle.draw(pyglet.gl.GL_TRIANGLES)

pyglet.clock.schedule_interval(update,timedelta)
pyglet.app.run()
