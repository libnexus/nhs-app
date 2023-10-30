from tkinter import Scrollbar, LabelFrame, Frame, Y, RIGHT, BOTH, YES
import application.data.service as sv


class ServicePreview(Frame):
    def __init__(self, master, service: sv.Service, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._service_object = service


class ServiceListbox(LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, text="Results", *args, **kwargs)
        self._services: list[sv.Service, ...] = []
        self._scrollbar = Scrollbar(self)
        self._scrollbar.pack(fill=Y, side=RIGHT)
        self._dummy = Frame(self, width=300, height=300)
        self._dummy.pack(expand=YES, fill=BOTH)
