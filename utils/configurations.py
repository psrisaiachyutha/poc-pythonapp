from utils.constants import (
    SQLITE_BD_FILE_PATH,
    REPORTS_META_DATA_TABLE_NAME,
    REPORTS_META_DATA_TABLE_CREATION_QUERY
)
from utils.sqlitehelper import create_database, create_table


def configure_required_db():
    create_database(SQLITE_BD_FILE_PATH)
    create_table(SQLITE_BD_FILE_PATH,
                 REPORTS_META_DATA_TABLE_NAME,
                 REPORTS_META_DATA_TABLE_CREATION_QUERY)
