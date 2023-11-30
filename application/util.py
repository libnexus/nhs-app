from json import loads

from application.data.persistent_storage import APP_CONFIG


def repair_config_file():
    CONFIG_ITEMS = {
        "SQL:CREATE": lambda: APP_CONFIG.__setitem__("SQL:CREATE", [
            "CREATE TABLE IF NOT EXISTS `service` ( `postcode` VARCHAR(12),`name` VARCHAR(200),"
            "`addr1` VARCHAR(150),`addr2` VARCHAR(150),`email` VARCHAR(320),"
            "`telephone` VARCHAR(15),`type` VARCHAR(20));",
            "CREATE TABLE IF NOT EXISTS `postcode` ( `postcode` VARCHAR(12) PRIMARY KEY, "
            "`longitude` FLOAT, `latitude` FLOAT );"]),
        "FILE:RECENT": lambda: APP_CONFIG.__setitem__("FILE:RECENT", [])
    }

    for key, propagator in CONFIG_ITEMS.items():
        if key not in APP_CONFIG:
            propagator()


postcodes: dict = loads(open("database-files/ll-postcodes.json", "r").read())
services: dict = loads(open("database-files/services-info.json", "r").read())


def generate_db_insertions() -> list[str, ...]:
    import JSONDatabaseIntermediary as jdbi
    statements = []

    db = jdbi.JSONDatabaseIntermediary()
    db.init_db()

    for postcode in db.postcodes():
        statements.append("INSERT INTO `postcode` (`postcode`, `longitude`, `latitude`) VALUES (\"%s\", %s, %s);" % (
            postcode.postcode, postcode.longitude, postcode.latitude))

    for service in db.services():
        statements.append(
            "INSERT INTO `service` (`postcode`, `name`, `addr1`, `addr2`, `email`, `telephone`, `type`) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");" % (
                service.postcode.postcode, service.name, service.address_line_1, service.address_line_2, service.email,
                service.telephone,
                service.service_type.upper()
            ))

    return statements
