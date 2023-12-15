import unittest

from SQLDatabaseIntermediary import SQLDatabaseIntermediary
from application.data.postcode import Postcode
from application.data.service import Service


class IntermediaryTest(unittest.TestCase):
    Connector: SQLDatabaseIntermediary | None = None

    def test_create_connector(self):
        connector = SQLDatabaseIntermediary()
        self.assertIsNot(connector, None)
        self.assertEqual(connector.init_db(), True)
        connector.close_db()

    """
    EXAMPLE POSTCODE AND SERVICE IN USE:
    LL573PL,"Ysgol Abercaseg (Babanod)",Abercaseg,bercaseg,"",01248 600194,SCHOOL
    """

    def test_get_all_postcodes(self):
        """
        finds all postcodes in database using the number of postcodes as the input
        """
        self.assertEqual(len(IntermediaryTest.Connector.get_all_postcodes()), 24_557)

    def test_get_postcode(self):
        """
        finds a specific postcode using postcode name, longitude, and latitude
        """
        self.assertIs(IntermediaryTest.Connector.get_postcode("LL573PL"),
                      Postcode("LL573PL", -4.0530610000000005, 53.177014))

    def test_get_services(self):
        """
        finds all services of a type using it's service type (such as school), postcode,
        and distance (distance being the farthest distance from the given postcode or coordinates)
        """
        self.assertEqual(
            len(IntermediaryTest.Connector.get_services("SCHOOL", IntermediaryTest.Connector.get_postcode("LL573PL"),
                                                        .05)), 7)

    def test_add_postcode(self):
        """
        adds a postcode using postcode name, longitude, and latitude. also checks if postcode already exists in database.
        """
        self.assertEqual(IntermediaryTest.Connector.get_postcode("LL581NZ"), SQLDatabaseIntermediary.POSTCODE_NOT_EXIST)
        IntermediaryTest.Connector.add_postcode(Postcode("LL581NZ", 0, 0))
        self.assertEqual(IntermediaryTest.Connector.get_postcode("LL581NZ"), SQLDatabaseIntermediary.POSTCODE_EXIST)

    def test_add_service(self):
        """
        adds a service to the database using a postcode, service name, addressline 1,
        addressline 2, their email, the telephone number, and the type of service
        """
        self.assertEqual(IntermediaryTest.Connector.get_service_by_name("Ysgol Abercaseg (Babanod)"),
                         SQLDatabaseIntermediary.DONT_KNOW_SERVICE)
        IntermediaryTest.Connector.add_service(
            name := Service(IntermediaryTest.Connector.get_postcode("LL573PL"), "name", "address line 1",
                            "address line 2", "email", "00000000", "GP"))
        self.assertIsInstance(IntermediaryTest.Connector.get_service_by_name("name"), Service)
        IntermediaryTest.Connector.del_service(name)
        self.assertEqual(IntermediaryTest.Connector.get_service_by_name("name"), 0)

    def test_update_service(self):
        service = IntermediaryTest.Connector.get_service_by_name("Ysgol Abercaseg (Babanod)")
        IntermediaryTest.Connector.update_service(service, "Ysgol Abercaseg (Babanod)", "123@outlook.com",
                                                  "00000000")

    def test_add_del_postcode(self):
        self.assertIsNotNone(postcode := IntermediaryTest.Connector.get_postcode("LL573PL"))
        IntermediaryTest.Connector.del_postcode(Postcode("LL573PL", 0, 0))
        self.assertEqual(IntermediaryTest.Connector.get_postcode("LL573PL"), 0)
        IntermediaryTest.Connector.add_postcode(postcode)
        self.assertIs(IntermediaryTest.Connector.get_postcode("LL573PL"), postcode)

    def test_add_del_service(self):
        self.assertIsInstance(school := IntermediaryTest.Connector.get_service_by_name("Ysgol Abercaseg (Babanod)"),
                              Service)
        IntermediaryTest.Connector.del_service(school)
        self.assertEqual(IntermediaryTest.Connector.get_service_by_name("Ysgol Abercaseg (Babanod)"), 0)
        IntermediaryTest.Connector.add_service(school)
        self.assertIs(IntermediaryTest.Connector.get_service_by_name("Ysgol Abercaseg (Babanod)"), school)


IntermediaryTest.Connector = SQLDatabaseIntermediary()
IntermediaryTest.Connector.init_db()

if __name__ == "__main__":
    unittest.main()
