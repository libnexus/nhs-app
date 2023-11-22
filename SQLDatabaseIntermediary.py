import sqlite3
from typing import Collection

from application.data import postcode as pc, service as sv
from application.data.db_connector import DatabaseIntermediary


class DBConnector(DatabaseIntermediary):
    """
    Class created by Ynyr with methods written by various members
    """

    def __init__(self):
        """
        Ynyr
        """
        self.connection: sqlite3.Connection | None = None

    def init_db(self) -> bool:
        """
        Ynyr
        """
        self.connection = sqlite3.connect("dbtest.db")
        return True

    def close_db(self) -> bool:
        """
        Ynyr
        """
        if self.is_connected:
            self.connection.close()
        return True

    @property
    def is_connected(self) -> bool:
        """
        Ynyr
        """
        return self.connection is not None

    @property
    def command_able(self) -> bool:
        """
        Ynyr
        """
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT 1 FROM Postcode")
        except sqlite3.Error:
            return False
        return True

    def get_all_postcodes(self, outcode: str | None = None) -> Collection[pc.Postcode, ...]:
        """
        Cameron
        """
        if not self.is_connected:
            return []

        cur = self.connection.cursor()

        if outcode is not None:
            cur.execute(f"SELECT * FROM Postcodes WHERE Postcode LIKE '{outcode}%' ")
        else:
            cur.execute("SELECT * FROM Postcodes")

        results = cur.fetchall()
        Postcodes = []

        for result in results:
            Postcodes.append(pc.Postcode(result, result[1], result[2]))

        return Postcodes

    def get_postcode(self, postcode: str) -> pc.Postcode | DatabaseIntermediary.POSTCODE_NOT_EXIST:
        """
        Ricardo
        """
        if not self.is_connected:
            return DatabaseIntermediary.POSTCODE_NOT_EXIST

        cur = self.connection.cursor()
        cur.execute("SELECT * FROM Postcode WHERE postcode = '%s'" % postcode)
        results = cur.fetchall()

        if not results:
            return DatabaseIntermediary.POSTCODE_NOT_EXIST

        _postcode = results[0]
        return pc.Postcode(postcode, _postcode[1], _postcode[2])

    def get_services(self,
                     service_type: str,
                     longitude: float,
                     latitude: float,
                     distance: float,
                     distance_from_postcode: pc.Postcode | None = None,
                     distance_from_coordinates: tuple[float, float] | None = None, max_number=0
                     ) -> DatabaseIntermediary.DONT_KNOW_SERVICE | Collection[sv.Service, ...]:
        if not self.is_connected:
            return []

        cur = self.connection.cursor()
        cur.execute(
            f"""
            SELECT * FROM Service 
            WHERE longitude < {longitude + distance} AND latitude < {latitude} + 1 
            AND {longitude - 1} < longitude AND {latitude}"""
        )

    """vvv Ricardo vvv"""

    def add_service(self, service: sv.Service):
        
        if not self.is_connected:
            return []

        cur = self.connection.cursor()
        cur.execute("""INSERT INTO Service (postcode, name, address_line_1, address_line_2, email, telephone, service_type) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" 
        %(service.postcode.postcode, service.name, service.address_line_1, service.address_line_2, service.email, service.telephone, service.service_type)) 
        

    def add_postcode(self, postcode: pc.Postcode) -> DatabaseIntermediary.POSTCODE_EXIST | None:
        
        if not self.is_connected:
            return POSTCODE_EXIST
        
        cur = self.connection.cursor() 
        cur.execute("""INSERT INTO Postcode VALUES ('%s')"""
        %(postcode.postcode))       
        

    def update_service(self, service: sv.Service, name: str, email: str, phonenumber: int) -> sv.Service:
        
        if not self.is_connected:
            return POSTCODE_EXIST

        cur = self.connection.cursor()
        cur.execute("""UPDATE Service (postcode, name, address_line_1, address_line_2, email, telephone, service_type) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" 
        %(service.postcode.postcode, service.name, service.address_line_1, service.address_line_2, service.email, service.telephone, service.service_type))

    def del_postcode(self, postcode: pc.Postcode) -> DatabaseIntermediary.POSTCODE_NOT_EXIST | DatabaseIntermediary.FAILED_TO_DELETE | None:
       
        if not self.is_connected:
            return POSTCODE_NOT_EXIST
        
        cur = self.connection.cursor() 
        cur.execute("""DELETE FROM Postcode VALUES ('%s')"""%(postcode.postcode))

    def del_service(self, service: sv.Service) -> DONT_KNOW_SERVICE | FAILED_TO_DELETE | None:
        
        if not self.is_connected:
            return DONT_KNOW_SERVICE

        cur = self.connection.cursor()
        cur.execute("""DELETE FROM Service WHERE Serviceid ='%s'"""%Serviceid)
