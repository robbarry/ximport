import csv

import pandas as pd
import numpy as np
import attr


measurer = np.vectorize(len)


@attr.s
class RowData:
    fields = attr.ib(factory=list)
    types = attr.ib(factory=dict)
    lengths = attr.ib(factory=dict)

    def update(self, field, column):
        if field not in self.fields:
            self.fields.append(field)
        self.update_type(field, column.dtype)
        if self.types[field] == "object":
            max_length = np.max(measurer(column.astype(str)))
            self.lengths[field] = self.lengths.get(field, None)
            if self.lengths[field] is None or self.lengths[field] < max_length:
                self.lengths[field] = max_length
        else:
            self.lengths[field] = self.lengths.get(field, None)

    def update_type(self, field, dtype):
        levels = {
            "object": 10,
            "float64": 5,
            "int64": 2,
        }
        self.types[field] = self.types.get(field, "int64")
        if levels[str(dtype)] > levels[self.types[field]]:
            self.types[field] = str(dtype)

    def sql(self, tablename="table"):
        sql_remap = {"int64": "int", "float64": "float", "object": "nvarchar"}
        create = []
        sub_create = []
        if "." in tablename:
            parts = tablename.split(".")
            tablename = f"[{parts[0]}].dbo.[{parts[1]}]"
        else:
            tablename = f"[{tablename}]"
        create.append(f"CREATE TABLE {tablename}")
        for field in self.fields:
            if self.lengths[field] is not None:
                sub_create.append(
                    f"[{field}] {sql_remap[self.types[field]]}({self.lengths[field]})"
                )
            else:
                sub_create.append(f"[{field}] {sql_remap[self.types[field]]}")
        create.append("({})".format(",\n".join(sub_create)))
        return "\n".join(create)


@attr.s
class ImportFile:
    filename = attr.ib()
    chunksize = attr.ib()
    rowcount = attr.ib(default=0)

    @classmethod
    def from_args(cls, args):
        return cls(filename=args.filename, chunksize=args.chunksize)

    def analyze(self):
        self.rowdata = RowData()
        for chunk in pd.read_csv(
            self.filename,
            chunksize=self.chunksize,
        ):
            self.rowcount += len(chunk)
            self._analyze(chunk)

    def _analyze(self, chunk):
        for column in chunk.columns:
            self.rowdata.update(column, chunk[column])


if __name__ == "__main__":
    pass
