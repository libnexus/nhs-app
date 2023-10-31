from tkinter import Scrollbar, LabelFrame, Frame, Y, RIGHT, BOTH, YES, VERTICAL, NW, Canvas
import application.data.service as sv


class ServicePreview(Frame):
    def __init__(self, master, service: sv.Service, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._service_object = service


class ServiceListbox(LabelFrame):
    def __init__(self, master, width: int, height: int, *args, **kwargs):
        super().__init__(master, width=width, height=height, text="Results", *args, **kwargs)
        self._services: list[sv.Service, ...] = []
        self._display_frame = ScrollableFrame(self, width, height, 0, 600)


class ScrollableFrame(Frame):
    """
    Scrollable frame object created by libnexus originally for another tkinter application
    """
    def __init__(self, master, width: int, height: int, scx: int, scy: int, *args, **kwargs):
        """
        Constructor for the scrollable frame object

        :param master: The master frame to which this frame is a slave
        :param width: the width of the frame; required so canvas can mimic it's dimensions
        :param height: the height of the frame; required so canvas can mimic its dimensions
        :param scx: the maximum scrolling x that can be scrolled to
        :param scy: the maximum scrolling y that can be scrolled to
        :param args: any positional arguments for the frame class
        :param kwargs: any keyword arguments for the frame class
        """
        super().__init__(master, *args, **kwargs)
        self._canvas = Canvas(master, width=width, height=height, scrollregion=(0, 0, scx, scy))
        self._display_frame = Frame(self._canvas)
        self._scrollbar = Scrollbar(master, orient=VERTICAL)
        self._canvas.create_window((0, 0), window=self._display_frame, anchor=NW)
        self._scrollbar.pack(side=RIGHT, fill=Y)
        self._scrollbar.config(command=self._canvas.yview)
        self._canvas.config(yscrollcommand=self._scrollbar.set)
        self._canvas.pack(expand=YES, fill=BOTH)
