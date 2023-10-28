from tkinter import Toplevel
import application.postcodes.postcode as pc
import application.postcodes.db_connector as dbc


class ServiceInformationEntry(Toplevel):
    def __init__(self, master, postcode: str, database_connector: dbc.DatabaseIntermediary):
        super().__init__(master)
        self._postcode = postcode 
        self._dbc = database_connector
