def color10():
    from cycler import cycler
    global blue, red, green, pink, purple, wine, yellow, ash, brown, orange
    red = "#e7287e"
    blue = "#62a3ff"
    green = "#156155"
    brown = "#461a0a"
    wine = "#9d1309"
    yellow = "#dab70b"
    orange = "#c15800"
    ash = "#b39675"
    purple = "#490092"
    pink = "#feb6db"
    colors = [blue, red, green, pink, purple, wine, yellow, ash, brown, orange]
    print("You can use blue, red, green, pink, purple, wine, yellow, ash, brown, and orange.")
    cc = cycler('color',colors)
    for ax in [a for f in figs for a in f.axes]:
        ax.set_prop_cycle(cc)

def default_color():
    from cycler import cycler
    global red, blue, green, purple, orange, gray, yellow
    red = "#c03a2b"
    blue = "#297fb9"
    green = "#16a084"
    purple = "#8e44ad"
    orange = "#f39d12"
    yellow = "#2c3e50"
    gray = "#aaaaaa"
    colors = [red,blue,green,purple,orange,yellow,gray]
    cc = cycler('color',colors)
    for ax in [a for f in figs for a in f.axes]:
        ax.set_prop_cycle(cc)

def gradient_color():
    global g1,g2,g3,g4,b1,b2,y1,y2,r1,r2,r3,r4
    g1 = "#007158"
    g2 = "#16a085"
    g3 = "#5ad2b5"
    g4 = "#8fffe7"
    b1 = "#202452"
    b2 = "#314c7f"
    y1 = "#f39c12"
    y2 = "#ffcd4e"
    r1 = "#c0392b"
    r2 = "#f96b55"
    r3 = "#ff9c82"
    r4 = "#ffd0b2"

def ppt(fs=18):
    set_fontsize(fs)
    set_font("Arial")
    set_framewidth(1.0)
    set_all_linewidth(1.5)
    set_all_markersize(8)
    set_all_markeredgewidth(1.5)

def pptfull(fig=None):
    if fig == None:
        fig = fig0
    ppt()
    set_axsize(20,13,fig)

def ppthalf(fig=None):
    if fig == None:
        fig = fig0
    ppt()
    set_axsize(10,14,fig)

def abst(fig=None):
    if fig == None:
        fig = fig0
    set_fontsize(10)
    set_font("Arial")
    set_framewidth(0.25)
    set_all_linewidth(0.5)
    set_all_markersize(3)
    set_all_markeredgewidth(0.25)
    set_axsize(8,5,fig)
    for ax in fig.axes:
        ax.tick_params(length=2)

def singlecolumn(fig=None):
    if fig == None:
        fig = fig0
    set_font("Arial")
    set_fontsize(8)
    set_framewidth(0.25)
    set_all_linewidth(0.5)
    set_all_markersize(3)
    set_all_markeredgewidth(0.5)
    for ax in fig.axes:
        ax.tick_params(length=2)
    set_axsize(6.5,4,fig)

default_color()