from __future__ import annotations

import sqlite3
from typing import Collection

import application.data.persistent_storage as pss
from application.data import postcode as pc, service as sv
from application.data.db_connector import DatabaseIntermediary


class SQLDatabaseIntermediary(DatabaseIntermediary):
    """
    Class created by Ynyr with methods written by various members
    """

    def __init__(self):
        """
        Ynyr
        """
        self.connection: sqlite3.Connection | None = None

    def init_db(self) -> bool:
        # if this is being run on a machine and not in the executable, comment out the below line and replace it with
        # the one that follows it, vice-versa
        self.connection = sqlite3.connect(pss.safe_path("postcode-service.db"))
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
            cur.execute(f"SELECT * FROM `postcode` WHERE `postcode` LIKE '{outcode}%' ")
        else:
            cur.execute("SELECT * FROM `postcode`")

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
        cur.execute("SELECT * FROM `postcode` WHERE postcode=\"%s\"" % postcode)
        results = cur.fetchall()

        if not results:
            return DatabaseIntermediary.POSTCODE_NOT_EXIST

        _postcode = results[0]
        return pc.Postcode(postcode, _postcode[1], _postcode[2])

    def get_services(self,
                     service_type: str,
                     postcode: pc.Postcode,
                     distance: float,
                     ) -> DatabaseIntermediary.DONT_KNOW_SERVICE | Collection[sv.Service, ...]:
        if not self.is_connected:
            return []

        cur = self.connection.cursor()
        cur.execute(
            f"""
            SELECT postcode.postcode, name, addr1, addr2, email, telephone, type 
            FROM service, postcode
            WHERE service.postcode=postcode.postcode AND service.type="{service_type}"
            AND longitude < {postcode.longitude} + {distance} 
            AND longitude > {postcode.longitude} - {distance} 
            AND latitude < {postcode.latitude} + {distance} 
            AND latitude > {postcode.latitude} - {distance}"""
        )
        results = cur.fetchall()
        services = []
        for serv in results:
            postcode, name, addr1, addr2, email, telephone, stype = serv
            service = sv.Service(self.get_postcode(postcode), name, addr1, addr2, email, telephone, stype)
            services.append(service)

        return services

    """vvv Ricardo vvv"""

    def add_service(self, service: sv.Service):

        if not self.is_connected:
            return []

        cur = self.connection.cursor()
        cur.execute(
            """INSERT INTO service (`postcode`, `name`, `addr1`, `addr2`, `email`, `telephone`, `type`) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")"""
            % (service.postcode.postcode, service.name, service.address_line_1, service.address_line_2, service.email,
               service.telephone, service.service_type))
        self.connection.commit()

    def add_postcode(self, postcode: pc.Postcode) -> DatabaseIntermediary.POSTCODE_EXIST | None:

        if not self.is_connected:
            return DatabaseIntermediary.POSTCODE_EXIST

        cur = self.connection.cursor()
        cur.execute("""INSERT INTO postcode (`postcode`, `longitude`, `latitude`) VALUES (\"%s\", %s, %s)"""
                    % (postcode.postcode, postcode.longitude, postcode.latitude))
        self.connection.commit()

    def update_service(self, service: sv.Service, name: str | None = None, email: str | None = None,
                       phonenumber: int | None = None) -> sv.Service:

        if not self.is_connected:
            return DatabaseIntermediary.POSTCODE_EXIST

        cur = self.connection.cursor()
        names, query = [], []
        if name:
            names.append("name")
            query.append(name)
        if email:
            names.append("email")
            query.append(email)
        if phonenumber:
            names.append("telephone")
            query.append(phonenumber)
        query = "UPDATE `service` SET %s WHERE `name`=\"%s\"" % (
            ", ".join(["`%s`=\"%s\"" % (k, v) for k, v in zip(names, query)]), service.name)
        cur.execute(query)
        self.connection.commit()

    def del_postcode(self,
                     postcode: pc.Postcode) -> DatabaseIntermediary.POSTCODE_NOT_EXIST | DatabaseIntermediary.FAILED_TO_DELETE | None:

        if not self.is_connected:
            return DatabaseIntermediary.POSTCODE_NOT_EXIST

        cur = self.connection.cursor()
        cur.execute("""DELETE FROM postcode WHERE `postcode`.`postcode`=\"%s\"""" % postcode.postcode)
        self.connection.commit()

    def del_service(self,
                    service: sv.Service) -> DatabaseIntermediary.DONT_KNOW_SERVICE | DatabaseIntermediary.FAILED_TO_DELETE | None:

        if not self.is_connected:
            return DatabaseIntermediary.DONT_KNOW_SERVICE

        cur = self.connection.cursor()
        cur.execute("""DELETE FROM service WHERE `name`.`name`=\"%s\"""" % service.name)
        self.connection.commit()

    def get_service_by_name(self, name: str) -> sv.Service:
        if not self.is_connected:
            return DatabaseIntermediary.DONT_KNOW_SERVICE

        cur = self.connection.cursor()
        cur.execute("""SELECT * FROM `service` WHERE `name`=\"%s\"""" % name)
        results = cur.fetchall()
        if not results:
            return DatabaseIntermediary.DONT_KNOW_SERVICE
        else:
            postcode, name, addr1, addr2, email, telephone, stype = results[0]
            return sv.Service(self.get_postcode(postcode), name, addr1, addr2, email, telephone, stype)
