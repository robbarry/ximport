import json
import os
import argparse

def get_last_arg(argument_name):
    try:
        with open(".ximport.cfg", "r") as f:
            return json.load(f)[argument_name]
    except:
        return None


def load_args(args):
    if not args.reset:
        for k, v in args.__dict__.items():
            if v is None and get_last_arg(k) is not None:
                args.__dict__[k] = get_last_arg(k)
    return args


def save_args(args):
    with open(".ximport.cfg", "w") as f:
        json.dump(args.__dict__, f)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Filename (eg: titanic3.csv)")
    parser.add_argument(
        "--dsn",
        "-d",
        help="DSN name (defined in freetds.conf, ex: DATA1)",
    )
    parser.add_argument(
        "--server",
        "-s",
        help="Server (ex: 10.1.12.9)",
    )
    parser.add_argument(
        "--database",
        "-db",
        help="Database (ex: database)",
    )
    
    parser.add_argument(
        "--table",
        "-t",
        help="Table (ex: main)",
    )

    parser.add_argument(
        "--username",
        "-u",
        default=os.getenv("SQL_USERNAME"),
        help="Defaults to .env :: SQL_USERNAME"
    )
    parser.add_argument(
        "--password",
        "-p",
        default=os.getenv("SQL_PASSWORD"),
        help="Defaults to .env :: SQL_PASSWORD"
    )
    parser.add_argument("--tds_version", default="7.4")
    parser.add_argument("--port", default=1433)
    parser.add_argument("--driver", default="/usr/local/lib/libtdsodbc.so")
    parser.add_argument("--create", action="store_true", help="Create table")
    parser.add_argument(
        "--drop", action="store_true", help="Drop table if it already exists"
    )
    parser.add_argument(
        "--reset", action="store_true", help="Do not load previous arguments"
    )
    parser.add_argument(
        "--chunksize", default=1000, help="Number of CSV lines to process in chunks"
    )
    args = load_args(parser.parse_args())
    save_args(args)
    return args
