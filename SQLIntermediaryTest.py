import unittest

from SQLDatabaseIntermediary import DBConnector
from application.data.postcode import Postcode
from application.data.service import Service


class IntermediaryTest(unittest.TestCase):
    def test_create_connector(self):
        self.connector = DBConnector()
        self.assertNotEquals(self.connector, None)
        self.assertIsNot(self.connector, None)

    def test_get_all_postcodes(self):
        """
        finds all postcodes in database
        """
        self.assertIs(self.connector.get_all_postcodes(outpost))

    def test_get_postcode(self):
        """
        finds a specific postcode using postcode name, longitude, and latitude
        """
        self.assertIs(self.connector.get_postcode("LL571NZ"), Postcode("LL571NZ", -4.12861, 53.22430799999999))

    def test_get_services(self):
        """
        finds a service using it's service type (such as school), postcode,
        and distance (distance being the farthest distance from the given postcode or coordinates)

        LL573PL,Ysgol Abercaseg (Babanod),Abercaseg,bercaseg,"",01248 600194,SCHOOL
        """
        self.assertIs(self.connector.get_services("SCHOOL", "LL573PL", ...))

    def test_add_postcode(self):
        """
        adds a postcode using postcode name, longitude, and latitude. also checks if postcode already exists in database.
        """
        self.assertEquals(self.connector.get_postcode("LL581NZ"), DBConnector.POSTCODE_NOT_EXIST)
        self.connector.add_postcode(Postcode("LL581NZ", 0, 0))
        self.assertEquals(self.connector.get_postcode("LL581NZ"), DBConnector.POSTCODE_EXIST)

    def test_add_service(self):
        """
        adds a service to the database using a postcode, service name, addressline 1,
        addressline 2, their email, the telephone number, and the type of service
        """
        self.assertEquals(self.connector.get_services("GP", "LL571NZ", ...), DBConnector.DONT_KNOW_SERVICE)
        self.connector.add_service(Service("LL571NZ", ..., ..., ..., ..., ..., "GP"))

    def test_update_service(self):
        ...

    def test_del_postcode(self):
        self.assertEquals(self.connector.get_postcode("QQ558FG"), DBConnector.POSTCODE_NOT_EXIST)
        self.connector.del_postcode(Postcode("QQ558FG", 0, 0))
        self.assertIsInstance(self.connector.get_postcode("QQ558FG"), Postcode)

    def test_del_service(self):
        self.assertEquals(DBConnector.get_service_by_name(...), DBConnector.DONT_KNOW_SERVICE)
        self.connector.del_service(DBConnector.get_service_by_name(...))
        self.assertIsInstance(self.connector.get_services(..., ..., ...), Service)



if __name__ == "__main__":
    unittest.main()
