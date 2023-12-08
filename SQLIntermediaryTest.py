import unittest

from SQLDatabaseIntermediary import SQLDatabaseIntermediary
from application.data.postcode import Postcode
from application.data.service import Service

connector: SQLDatabaseIntermediary | None = None


class IntermediaryTest(unittest.TestCase):
    def test_create_connector(self):
        global connector

        connector = SQLDatabaseIntermediary()
        self.assertIsNot(connector, None)

    """
    EXAMPLE POSTCODE AND SERVICE IN USE:
    LL573PL,"Ysgol Abercaseg (Babanod)",Abercaseg,bercaseg,"",01248 600194,SCHOOL
    """

    def test_get_all_postcodes(self):
        """
        finds all postcodes in database using the number of postcodes as the input
        """
        self.assertEquals(len(connector.get_all_postcodes()), 24_557)

    def test_get_postcode(self):
        """
        finds a specific postcode using postcode name, longitude, and latitude
        """
        self.assertIs(connector.get_postcode("LL573PL"), Postcode("LL573PL", -4.0530610000000005, 53.177014))

    def test_get_services(self):
        """
        finds all services of a type using it's service type (such as school), postcode,
        and distance (distance being the farthest distance from the given postcode or coordinates)
        """
        self.assertIs(connector.get_services("SCHOOL", connector.get_postcode("LL573PL"), 1), ...)

    def test_add_postcode(self):
        """
        adds a postcode using postcode name, longitude, and latitude. also checks if postcode already exists in database.
        """
        self.assertEquals(connector.get_postcode("LL581NZ"), SQLDatabaseIntermediary.POSTCODE_NOT_EXIST)
        connector.add_postcode(Postcode("LL581NZ", 0, 0))
        self.assertEquals(connector.get_postcode("LL581NZ"), SQLDatabaseIntermediary.POSTCODE_EXIST)

    def test_add_service(self):
        """
        adds a service to the database using a postcode, service name, addressline 1,
        addressline 2, their email, the telephone number, and the type of service
        """
        self.assertEquals(connector.get_service_by_name("Ysgol Abercaseg (Babanod)"), SQLDatabaseIntermediary.DONT_KNOW_SERVICE)
        connector.add_service(Service(connector.get_postcode("LL573PL"), "name", "address line 1",
                                      "address line 2", "email", "00000000", "GP"))

    def test_update_service(self):
        service = connector.get_service_by_name("Ysgol Abercaseg (Babanod)")
        connector.update_service(service, ..., ..., ...)
        ...

    def test_del_postcode(self):
        self.assertEquals(connector.get_postcode("LL573PL"), SQLDatabaseIntermediary.POSTCODE_NOT_EXIST)
        connector.del_postcode(Postcode("LL573PL", 0, 0))
        self.assertIsInstance(connector.get_postcode("LL573PL"), Postcode)

    def test_del_service(self):
        self.assertEquals(connector.get_service_by_name("Ysgol Abercaseg (Babanod)"), SQLDatabaseIntermediary.DONT_KNOW_SERVICE)
        connector.del_service(connector.get_service_by_name("Ysgol Abercaseg (Babanod)"))
        self.assertIsInstance(connector.get_services("SCHOOL", connector.get_postcode("LL573PL"), 100_000), Service)


if __name__ == "__main__":
    unittest.main()
