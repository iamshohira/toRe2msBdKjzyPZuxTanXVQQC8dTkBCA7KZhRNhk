def set_axsize(w,h,fig=None):
    """set axis size

    Args:
        w (float): width in cm
        h (float): height in cm
        fig (Figure): target figure [defalut=figs[0]]
    """
    if fig == None:
        fig = fig0
    winch = w / 2.54
    hinch = h / 2.54
    now_winch, now_hinch = fig.get_size_inches()
    left_m = now_winch * fig.subplotpars.left
    right_m = now_winch * (1-fig.subplotpars.right)
    top_m = now_hinch * (1-fig.subplotpars.top)
    bottom_m = now_hinch * fig.subplotpars.bottom
    new_winch = left_m + winch + right_m
    new_hinch = top_m + hinch + bottom_m
    fig.canvas.resize(int(new_winch*72),int(new_hinch*72))
    fig.set_size_inches(new_winch,new_hinch)


def set_figsize(w,h,fig=None):
    """set figure size

    Args:
        w (float): width in cm
        h (float): height in cm
        fig (Figure): target figure [defalut=figs[0]]
    """
    if fig == None:
        fig = fig0
    winch = w / 2.54
    hinch = h / 2.54
    fig.set_size_inches(winch,hinch)
    fig.canvas.resize(int(winch*72),int(hinch*72))
    fig.set_size_inches(winch,hinch)


def set_framecolor(color, axis=None):
    """change frame, tick, and label colors of target axis

    Args:
        color (string): color name 
        axis (matplotlib.Axis, optional): target axis. If None, apply to all axis in figs.axes. Defaults to None.
    """
    if axis != None:
        axes = [axis]
    else:
        axes = [a for f in figs for a in f.axes]
    for axis in axes:
        axis.xaxis.label.set_color(color)
        axis.yaxis.label.set_color(color)
        axis.tick_params(colors=color,which='both')
        for i in ['left','right','top','bottom']:
            axis.spines[i].set_color(color)


def set_framewidth(width, axis=None):
    """change frame line width

    Args:
        width (float): linewidth 
        axis (matplotlib.Axis, optional): target axis. If None, apply to all axis in figs.axes. Defaults to None.
    """
    if axis != None:
        axes = [axis]
    else:
        axes = [a for f in figs for a in f.axes]
    for axis in axes:
        axis.tick_params(width=width,which='both')
        for i in ['left','right','top','bottom']:
            axis.spines[i].set_linewidth(width)


def set_fontsize(size,axis=None):
    """change font size of all components
    Args:
        size (int): fontsize
        axis (matplotlib.Axis, optional): target axis. If None, apply to all axis in figs.axes. Defaults to None.
    """
    if axis != None:
        axes = [axis]
    else:
        axes = [a for f in figs for a in f.axes]
    for axis in axes:
        axis.set_xlabel(axis.get_xlabel(),fontsize=size)
        axis.set_ylabel(axis.get_ylabel(),fontsize=size)
        axis.tick_params(labelsize=size)
        for t in axis.texts:
            t.set_fontsize(size)
        if axis.legend_:
            for text in axis.legend_.texts:
                text.set_fontsize(size)

def set_font(fontname,axis=None):
    """change font size of all components
    Args:
        fontname (str): fontname
        axis (matplotlib.Axis, optional): target axis. If None, apply to all axis in figs.axes. Defaults to None.
    """
    font = {'family':fontname}
    if axis != None:
        axes = [axis]
    else:
        axes = [a for f in figs for a in f.axes]
    for axis in axes:
        axis.set_xlabel(axis.get_xlabel(),**font)
        axis.set_ylabel(axis.get_ylabel(),**font)
        form = axis.xaxis.get_major_formatter()
        loca = axis.xaxis.get_major_locator()
        lim = axis.get_xlim()
        ticks = np.linspace(lim[0],lim[1],100)
        axis.xaxis.set_ticks(ticks)
        axis.xaxis.set_ticklabels(ticks,**font)
        axis.xaxis.set_major_formatter(form)
        axis.xaxis.set_major_locator(loca)
        form = axis.yaxis.get_major_formatter()
        loca = axis.yaxis.get_major_locator()
        lim = axis.get_ylim()
        ticks = np.linspace(lim[0],lim[1],100)
        axis.yaxis.set_ticks(ticks)
        axis.yaxis.set_ticklabels(ticks,**font)
        axis.yaxis.set_major_formatter(form)
        axis.yaxis.set_major_locator(loca)
        if axis.legend_:
            for text in axis.legend_.texts:
                text.set_fontname(fontname)
        for t in axis.texts:
            t.set_fontname(fontname)
        axis.title.set_fontname(fontname)

# def savefig_for_animation(baseplots, animationplots, axis=ax, framecolor='black'):
#     """write separated figures for graph animation in powerpoint

#     Args:
#         baseplots (List[matplotlib.Line2D]): List of matplotlib's plot data, which are drawn with the figure frame.
#         animationplots (List[List[matplotlib.Line2D]]): List of list of matplotlib's plot data, which are drawn without the figure frame.
#         axis (matplotlib.Axis, optional): target axis. Defaults to ax.
#         framecolor (str, optional): frame color applied after operation. Defaults to 'black'.
#     """
#     from PyQt6.QtWidgets import QFileDialog
#     import os
#     filte = "Encapsulated Postscript (*.eps);;Portable Network Graphics (*.png);;Portable Document Format (*.pdf);;Scalable Vector Graphics (*.svg)"
#     filename = QFileDialog.getSaveFileName(None,"Figure name",fig.canvas.get_default_filename(),filte,"Portable Document Format (*.pdf)")
#     if filename[0] == '':
#         return

#     prefix, ext = os.path.splitext(filename[0])
    
#     def set_visible_for_all(b):
#         for plot in axis.lines:
#             plot.set_visible(b)

#     set_visible_for_all(False)        
#     for plot in baseplots:
#         plot.set_visible(True)
#     fig.savefig('{0}{1:02d}{2}'.format(prefix,0,ext))

#     set_framecolor("none")
#     for i,plotlist in enumerate(animationplots):
#         set_visible_for_all(False)
#         for plot in plotlist:
#             plot.set_visible(True)
#         fig.savefig('{0}{1:02d}{2}'.format(prefix,i+1,ext))
    
#     set_visible_for_all(True)
#     set_framecolor(framecolor,axis=axis)


def set_all_linewidth(width,axis=None):
    """set linewidth for all plots in axis

    Args:
        width (float): line width
        axis (matplotlib.Axis, optional): target axis. If None, apply to all axis in figs.axes. Defaults to None.
    """
    if axis != None:
        axes = [axis]
    else:
        axes = [a for f in figs for a in f.axes]
    for axis in axes:
        for plot in axis.lines:
            plot.set_linewidth(width)


def set_all_marker(markers,axis=None):
    """set marker for all plots in axis

    Args:
        markers (List(str)): List of marker type
        axis ([type], optional): [description]. target axis. If None, apply to all axis in figs.axes. Defaults to None.
    """
    from itertools import cycle
    a = cycle(markers)
    if axis != None:
        axes = [axis]
    else:
        axes = [a for f in figs for a in f.axes]
    for axis in axes:
        for plot in axis.lines:
            m = next(a)
            plot.set_marker(m)


def set_all_markersize(size,axis=None):
    """set marker size for all plots in axis

    Args:
        size (float): marker size
        axis ([type], optional): [description]. target axis. If None, apply to all axis in figs.axes. Defaults to None.
    """
    if axis != None:
        axes = [axis]
    else:
        axes = [a for f in figs for a in f.axes]
    for axis in axes:
        for plot in axis.lines:
            plot.set_markersize(size)

def set_all_markeredgewidth(size,axis=None):
    """set marker size for all plots in axis

    Args:
        size (float): marker size
        axis ([type], optional): [description]. target axis. If None, apply to all axis in figs.axes. Defaults to None.
    """
    if axis != None:
        axes = [axis]
    else:
        axes = [a for f in figs for a in f.axes]
    for axis in axes:
        for plot in axis.lines:
            plot.set_markeredgewidth(size)

def font_dialog(axis=None):
    """Open dialog for font setting
    Args:
        axis (matplotlib.Axis, optional): target axis. If None, apply to all axis in fig.axes. Defaults to None.
    """
    from PyQt6.QtWidgets import QFontDialog
    from matplotlib import font_manager
    import difflib
    import os
    fm = font_manager.fontManager
    familylist = [f.name for f in fm.afmlist]
    familylist.extend([f.name for f in fm.ttflist])
    familylist = list(set(familylist))
    font, ok = QFontDialog.getFont()
    if ok:
        closest = difflib.get_close_matches(font.family(),familylist)
        if len(closest) == 0:
            print("Error!")
            print("Font family \"{}\" is not available in matplotlib!".format(font.family(),))
            print("Removing {} may solve the problem.".format(os.path.join(os.path.expanduser('~'),".matplotlib","fontlist-v***.json"),))
            return
        set_font(closest[0],axis)
        set_fontsize(font.pointSize(),axis)
        if closest[0] != font.family():
            print("Warning!")
            print("Font family \"{}\" was not included in the available list.".format(font.family(),))
            print("The closest \"{}\" was used instead.".format(closest[0]))
        print("Family name: {}".format(closest[0],))
        print("Point size : {}".format(font.pointSize(),))


class label:
    colorx = {}
    colory = {}

    @classmethod
    def off(cls,axis=None):
        """hide labels (not deleted)

        Args:
            axis (matplotlib.Axis, optional): target axis. If None, apply to all axis in figs.axes. Defaults to None.
        """
        if axis != None:
            axes = [axis]
        else:
            axes = [a for f in figs for a in f.axes]
        for axis in axes:
            cls.colorx[axis] = axis.xaxis.label.get_color()
            cls.colory[axis] = axis.yaxis.label.get_color()
            axis.xaxis.label.set_color("none")
            axis.yaxis.label.set_color("none")

    @classmethod
    def on(cls,axis=None):
        """show labels hided by label_off.

        Args:
            axis (matplotlib.Axis, optional): target axis. If None, apply to all axis in figs.axes. Defaults to None.
        """
        if axis != None:
            axes = [axis]
        else:
            axes = [a for f in figs for a in f.axes]
        for axis in axes:
            try:
                axis.xaxis.label.set_color(cls.colorx[axis])
                axis.yaxis.label.set_color(cls.colory[axis])
            except:
                axis.xaxis.label.set_color('k')
                axis.yaxis.label.set_color('k')


from matplotlib.ticker import MultipleLocator, AutoLocator, ScalarFormatter

class OffestMultipleLocator(MultipleLocator):
    def __init__(self,base,offset):
        self.offset = offset
        super().__init__(base)

    def tick_values(self, vmin, vmax):
        vmin -= self.offset
        vmax -= self.offset
        ticks = super().tick_values(vmin,vmax)
        return ticks + self.offset

    def view_limits(self, dmin, dmax):
        return super().view_limits(dmin, dmax)

class FloatToIntegerFomatter(ScalarFormatter):
    def __init__(self,numbers):
        self.numbers = numbers
        super().__init__()
    
    def __call__(self, x, pos=None):
        if x in self.numbers:
            return "%d" % x
        else:
            return super().__call__(x, pos=pos)

class set_ticks:
    @classmethod
    def x(cls, start, majorstep, minorstep=None, axis=None):
        """ set ticks of x axis

        Args:
            start (float): major ticks start from this value.
            majorstep ([float]): step width for major ticks
            minorstep (float, optional): step width for minor ticks. Defaults to None.
            axis ([type], optional): [description]. target axis. If None, apply to all axis in fig.axes. Defaults to None.
        """
        if axis != None:
            axes = [axis]
        else:
            axes = [a for f in figs for a in f.axes]
        for axis in axes:
            axis.xaxis.set_major_locator(OffestMultipleLocator(majorstep,start))
            if minorstep != None:
                axis.xaxis.set_minor_locator(OffestMultipleLocator(minorstep,start))

    @classmethod
    def y(cls, start, majorstep, minorstep=None, axis=None):
        """ set ticks of y axis

        Args:
            start (float): major ticks start from this value.
            majorstep ([float]): step width for major ticks
            minorstep (float, optional): step width for minor ticks. Defaults to None.
            axis ([type], optional): [description]. target axis. If None, apply to all axis in fig.axes. Defaults to None.
        """
        if axis != None:
            axes = [axis]
        else:
            axes = [a for f in figs for a in f.axes]
        for axis in axes:
            axis.yaxis.set_major_locator(OffestMultipleLocator(majorstep,start))
            if minorstep != None:
                axis.yaxis.set_minor_locator(OffestMultipleLocator(minorstep,start))

    @classmethod
    def initialize(cls, axis=None):
        """ revert to auto scale mode

        Args:
            axis ([type], optional): [description]. target axis. If None, apply to all axis in fig.axes. Defaults to None.
        """
        if axis != None:
            axes = [axis]
        else:
            axes = [a for f in figs for a in f.axes]
        for axis in axes:
            axis.xaxis.set_major_locator(AutoLocator())
            axis.xaxis.set_minor_locator(AutoLocator())
            axis.yaxis.set_major_locator(AutoLocator())
            axis.yaxis.set_minor_locator(AutoLocator())
            axis.xaxis.set_major_formatter(ScalarFormatter())
            axis.yaxis.set_major_formatter(ScalarFormatter())

    @classmethod
    def disp_as_int(cls,numbers,axis=None):
        """set numbers to be integer

        Args:
            numbers (List(int)): numbers to be integer
            axis ([type], optional): [description]. target axis. If None, apply to all axis in fig.axes. Defaults to None.
        """
        if axis != None:
            axes = [axis]
        else:
            axes = [a for f in figs for a in f.axes]
        for axis in axes:
            axis.xaxis.set_major_formatter(FloatToIntegerFomatter(numbers))
            axis.yaxis.set_major_formatter(FloatToIntegerFomatter(numbers))
        
    @classmethod
    def offset(cls, b, axis=None):
        """set offset representation of ticks

        Args:
            b (Bool): turn False if you don't want to use offset
            axis ([type], optional): [description]. target axis. If None, apply to all axis in fig.axes. Defaults to None.
        """
        if axis != None:
            axes = [axis]
        else:
            axes = [a for f in figs for a in f.axes]
        for axis in axes:
            axis.xaxis.get_major_formatter().set_useOffset(b)
            axis.yaxis.get_major_formatter().set_useOffset(b)

    # compatibility
    @classmethod
    def tointeger(cls,numbers,axis=None):
        cls.disp_as_int(numbers,axis)
        
    #compatibility
    def auto(cls,axis=None):
        cls.initialize(axis)
        
# compatibility
ticks_offset = lambda b, axis=None: set_ticks.offset(b, axis)
