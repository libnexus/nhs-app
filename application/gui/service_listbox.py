from tkinter import Scrollbar, LabelFrame, Frame, X, Y, RIGHT, BOTH, YES, NO, VERTICAL, NW, Canvas, NSEW, Label
import application.data.service as sv
import application.data.postcode as pc


class ServicePreview(Frame):
    def __init__(self, master, service: sv.Service, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._service_object = service
        self._name = Label(self, text=service.name)
        self._email = Label(self, text=service.email)
        self._name.grid(row=0, column=0)
        self._email.grid(row=1, column=0)


class ServiceListbox(LabelFrame):
    def __init__(self, master, width: int, height: int, *args, **kwargs):
        super().__init__(master, width=width, height=height, text="Results", *args, **kwargs)
        self._services: list[sv.Service, ...] = []
        self._display_frame = ScrollableFrame(self, width, height, height * 10, padx=10, pady=20)
        self._service = ServicePreview(self._display_frame,
                                       sv.Service(pc.Postcode("LL001YZ", -42.209, 5.117), "Alpha Ind.",
                                                  "Some manner of address line 1",
                                                  "Some manner of address line 2",
                                                  "some-gp@bangor.ac.uk", "GP"))
        self._service.pack(expand=YES, fill=X)
        self._service.config(background="#00ff00")
        self._display_frame.canvas.pack(expand=YES, fill=BOTH)
        self._display_frame.pack(expand=YES, fill=BOTH)


class ScrollableFrame(Frame):
    def __init__(self, master, width, height, scy, *args, **kwargs):
        """
        Creates a scrollable frame for the Y axis which has a vertical scrollbar

        :param master: The master frame to which this frame is a slave
        :param width: the width of the frame; required so canvas can mimic it's dimensions
        :param height: the height of the frame; required so canvas can mimic its dimensions
        :param scy: the maximum scrolling y that can be scrolled to, is added to height
        :param args: any positional arguments for the frame class
        :param kwargs: any keyword arguments for the frame class
        """
        self._canvas = Canvas(master, width=width, height=height)
        self._canvas.config(scrollregion=(0, 0, width, height + scy))
        super().__init__(self._canvas, *args, **kwargs)
        self._scrollbar = Scrollbar(master, orient=VERTICAL)
        self._canvas.create_window((width, height), window=self, anchor=NW)
        self._canvas.config(yscrollcommand=self._scrollbar.set)
        self._scrollbar.config(command=self._canvas.yview)
        self._scrollbar.pack(side=RIGHT, fill=Y)

    @property
    def scrollbar(self) -> Scrollbar:
        return self._scrollbar

    @property
    def canvas(self) -> Canvas:
        return self._canvas
