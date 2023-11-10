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
        root.state("iconic")

        self._gp: Service | None = None
        self._dentist: Service | None = None
        self._optician: Service | None = None
        self._schools: list[Service, ...] = []

        # Menu

        self._menu = Menu(root)

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


main = Main(root)
main.pack(fill=BOTH, expand=YES)

root.mainloop()
