def ppt(fs=18):
    set_fontsize(fs)
    set_font("Myriad Pro")
    set_framewidth(1.0)
    set_all_linewidth(1.5)
    set_all_markersize(8)
    set_all_markeredgewidth(1.5)

def pptfull():
    ppt()
    set_axsize(20,13)

def ppthalf():
    ppt()
    set_axsize(10,14)

def abst():
    set_fontsize(10)
    set_font("Arial")
    set_framewidth(0.25)
    set_all_linewidth(0.5)
    set_all_markersize(3)
    set_all_markeredgewidth(0.25)
    set_axsize(8,5)
    for ax in fig.axes:
        ax.tick_params(length=2)

def singlecolumn():
    set_font("Arial")
    set_fontsize(8)
    set_framewidth(0.25)
    set_all_linewidth(0.5)
    set_all_markersize(3)
    set_all_markeredgewidth(0.5)
    for ax in fig.axes:
        ax.tick_params(length=2)
    set_axsize(6.5,4)


set_loader("plot",0)
bel = lambda: set_loader("belsorp")
