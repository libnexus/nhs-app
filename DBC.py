from typing import Collection

import application.data.db_connector as dbc
from application.data import postcode as pc, service as sv


class DB(dbc.DatabaseIntermediary):
    def __init__(self):
        pass

    def init_db(self) -> bool:
        return True

    def close_db(self) -> bool:
        return True

    @property
    def is_connected(self) -> bool:
        return True

    @property
    def command_able(self) -> bool:
        return True

    def get_all_postcodes(self, outcode: str | None = None) -> Collection[pc.Postcode, ...]:
        return []

    def get_postcode(self, postcode: str) -> pc.Postcode | dbc.DatabaseIntermediary.POSTCODE_NOT_EXIST:
        return dbc.DatabaseIntermediary.POSTCODE_NOT_EXIST

    def get_services(self, service_type: str, longitude: float, latitude: float, distance: float,
                     distance_from_postcode: pc.Postcode | None = None,
                     distance_from_coordinates: tuple[float, float] | None = None,
                     max_number=0) -> dbc.DatabaseIntermediary.DONT_KNOW_SERVICE | \
                                      Collection[
                                          sv.Service, ...]:
        pass
