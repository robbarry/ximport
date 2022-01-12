import os

from ximport.files import ImportFile
from ximport.arguments import get_args
from ximport.db import MSSQL, BCP
from ximport.log import get_logger
from dotenv import load_dotenv
from inspect import getsourcefile

load_dotenv(dotenv_path=os.path.join(os.path.dirname(getsourcefile(lambda:0)), ".env"))

log = get_logger(__name__)

if __name__ == "__main__":
    args = get_args()
    bcp = BCP.from_args(args)
    f = ImportFile.from_args(args, bcp)
    db = MSSQL.from_args(args)
    f.process()
    if args.create:
        if args.drop:
            db.cursor.execute("DROP TABLE [{}]".format(args.table))
        statement = f.rowdata.sql(args.table)
        log.info("Create statement: {}".format(statement))
        db.cursor.execute(statement)
        db.conn.commit()
    bcp.import_file()
    