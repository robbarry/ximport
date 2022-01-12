import os
import tempfile
from pathlib import Path
import shlex

import attr
import pyodbc

from ximport.log import get_logger

log = get_logger(__name__)

@attr.s
class MSSQL:
    conn = attr.ib()
    cursor = attr.ib()

    @classmethod
    def from_args(cls, args):
        if args.dsn:
            return cls.from_dsn(args.dsn, args.username, args.password)
        else:
            return cls.from_server(args.server, args.database, args.username, args.password, args.tds_version, args.port, args.driver)

    @classmethod
    def from_dsn(cls, dsn, uid, pwd):
        conn = pyodbc.connect(f"DSN={dsn};UID={uid};PWD={pwd}")
        return cls(conn = conn, cursor = conn.cursor())

    @classmethod
    def from_server(cls, server, database, user, password, tds_version = '7.4', port =1433, driver='FreeTDS'):
        conn = pyodbc.connect(
            server=server,
            database=database,
            user=user,
            tds_version=tds_version,
            password=password,
            port=port,
            driver=driver)        
        return cls(conn = conn, cursor = conn.cursor())

    def __exit__(self):
        try:
            self.cursor.close()
        except Exception as e:
            pass

        try:
            self.conn.close()
        except Exception as e:
            pass

@attr.s
class BCP:
    database_name = attr.ib()
    schema = attr.ib()
    table_name = attr.ib()
    server_name = attr.ib()
    username = attr.ib()
    password = attr.ib()
    inpath = attr.ib()
    infile = attr.ib()
    
    @classmethod
    def from_args(cls, args):
        return cls(database_name = args.database, schema = "dbo", table_name = args.table, server_name = args.server, username = args.username, password = args.password)

    @inpath.default
    def inpath_default(self):
        return tempfile.TemporaryDirectory()
        
    @infile.default
    def infile_default(self):
        return os.path.join(self.inpath.name, self.table_name)

    def import_file(self):
        statement = ["bcp", self.table_name, "in", self.infile,
                     "-S", self.server_name,
                     "-d", self.database_name,
                     "-U", self.username, "-P", self.password,
                     "-eerror.txt",
                     "-q",
                     "-c",
                     "-t" + chr(30),
                     "-r", "0x0a"
                     ]
        cmd = shlex.join(statement)
        log.info(f"BCP statement: {cmd}")
        os.system(cmd)

    def __exit__(self):
        self.inpath.cleanup()
