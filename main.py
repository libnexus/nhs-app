from tkinter import Tk, Frame, BOTH, YES, LabelFrame, Entry, Menu
from tkinter.messagebox import showerror

import JSONDatabaseIntermediary as jdbi
from application.gui.service_info_entry import ServiceInformationEntry
from application.data.service import Service

root = Tk()


def _service_info(service: Service):
    information = "    Name: %s\n" % service.name
    information += "    Address (1): %s\n" % service.address_line_1
    information += "    Address (2): %s\n" % service.address_line_2
    if service.email:
        information += "    Email: %s\n" % service.email
    if service.telephone:
        information += "    Tel: %s\n" % service.telephone
    information += "\n"
    return information


class Main(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._jdbi = jdbi.JSONDatabaseIntermediary()
        if not self._jdbi.init_db():
            showerror("Uh Oh", "The database had trouble connecting. Try restarting the program.")
            raise SystemExit

        self._gp: Service | None = None
        self._dentist: Service | None = None
        self._optician: Service | None = None
        self._schools: list[Service, ...] = []

        # Menu
        # ref: https://pythonspot.com/tk-menubar/
        self._menu = Menu(root)
        filemenu = Menu(self._menu, tearoff=0)
        filemenu.add_command(label="New", command=self._file_new)
        filemenu.add_command(label="Open", command=self._file_open)
        filemenu.add_command(label="Open recent", command=self._file_open_recent)
        filemenu.add_command(label="Save As", command=self._file_save_as)
        filemenu.add_command(label="Export", command=self._file_export)
        filemenu.add_command(label="Import", command=self._file_import)
        filemenu.add_separator()
        # Added exit option in menu, not needed but nice addition
        filemenu.add_command(label="Exit", command=root.quit)
        self._menu.add_cascade(label="File", menu=filemenu)

        formmenu = Menu(self._menu, tearoff=0)
        formmenu.add_command(label="Clear", command=self._form_clear)
        formmenu.add_command(label="Copy", command=self._form_copy)
        formmenu.add_separator()
        formmenu.add_command(label="Preview", command=self._form_preview)
        self._menu.add_cascade(label="Form",menu=formmenu)

        helpmenu = Menu(self._menu, tearoff=0)
        helpmenu.add_command(label="User Manual", command=self._help_user_manual)
        helpmenu.add_command(label="Version Info", command=self._help_version_info)
        self._menu.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=self._menu)



    def _compile_information_to_string(self) -> str:
        """
        Compiles the information given into a nice string which can then be exported to a txt file
        Modifications to this method may make it compile to html which can be converted to pdf
        """
        information = ""

        for name, service in zip(["GP", "Dentist", "Optician"], [self._gp, self._dentist, self._optician]):
            information += "Information for %s\n" % name
            information += _service_info(service)

        for i, school in enumerate(self._schools):
            information += "Child %ds school:" % i
            information += _service_info(school)

        return information

    def _file_new(self):
        pass

    def _file_open(self):
        pass

    def _file_open_recent(self):
        pass

    def _file_save(self):
        pass

    def _file_save_as(self):
        pass

    def _file_export(self):
        pass

    def _file_import(self):
        pass

    def _form_clear(self):
        pass

    def _form_copy(self):
        pass

    def _form_preview(self):
        pass

    def _help_user_manual(self):
        pass

    def _help_version_info(self):
        pass


main = Main(root)
main.pack(fill=BOTH, expand=YES)

root.mainloop()
