from tkinter import LabelFrame, Label, Canvas, Scrollbar, Frame, BOTH, LEFT, RIGHT, Y, NW, Event

import application.data.service as sv


class ServicePreview(Frame):
    def __init__(self, master, service: sv.Service, propagate_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._service_object = service
        self._name = Label(self, text=service.name)
        self._email = Label(self, text=service.postcode.nice_postcode)
        self._name.grid(row=0, column=0)
        self._email.grid(row=1, column=0)
        self._propagate_callback = propagate_callback
        self._name.bind("<Double-Button-1>", self.double_click)
        self._email.bind("<Double-Button-1>", self.double_click)

    def double_click(self, event: Event):
        self._propagate_callback(self._service_object)


class ServiceListbox(LabelFrame):
    def __init__(self, master, propagate_callback, *args, svw=200, **kwargs):
        """
        TODO docstring
        """
        super().__init__(master, text="Results", *args, **kwargs)
        self._services: list[sv.Service, ...] = []
        self._display_frame = ScrollView(self, width=svw)
        self._display_frame.pack(fill=BOTH, expand=0)
        self._propagate_callback = propagate_callback
        self._shown_services: list[ServicePreview, ...] = []

    def clear_services(self):
        for preview in self._shown_services:
            preview.destroy()
        self._shown_services.clear()
        self.update()

    def add_new_service(self, service: sv.Service):
        preview = ServicePreview(self._display_frame.scrollable_frame, service, self._propagate_callback)
        preview.pack(fill=Y, expand=False)
        self._shown_services.append(preview)
        self.update()


class ScrollView(Frame):
    """
    https://blog.teclado.com/tkinter-scrollable-frames/
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._canvas = Canvas(self, *args, **kwargs)
        self._scrollbar = Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._scrollable_frame = Frame(self._canvas)
        self._scrollable_frame.bind("<Configure>",
                                    lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.create_window((0, 0), window=self.scrollable_frame, anchor=NW)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.pack(side=LEFT, expand=False)
        self._scrollbar.pack(side=RIGHT, fill=Y)

    @property
    def scrollable_frame(self) -> Frame:
        return self._scrollable_frame

    @property
    def canvas(self) -> Canvas:
        return self._canvas
