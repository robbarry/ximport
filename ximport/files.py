import csv

import attr


@attr.s
class AutoType:
    name = attr.ib(default=None)
    value = attr.ib(default=None)
    type = attr.ib()
    length = attr.ib()
    level = attr.ib()

    @type.default
    def type_default(self):
        try:
            f = float(self.value)
            if f.is_integer():
                return "int"
            else:
                return "float"
        except:
            return "varchar"

    @length.default
    def length_default(self):
        if self.type == "varchar":
            return len(self.value)
        else:
            return None


@attr.s
class RowTypes:
    types = {}
    lengths = {}

    def update(self, type):
        if type.name not in types:
            self.types[type.name] = type
            self.lengths[type.name] = type.length
        else:
            


@attr.s
class ImportFile:
    filename = attr.ib()

    @classmethod
    def from_args(cls, args):
        return cls(
            filename=args.filename,
        )

    def analyze(self):
        self.get_
        with open(self.filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pass


if __name__ == "__main__":
    import time

    results = []
    vals = {
        "1": "int",
        "-1": "int",
        "1.1": "float",
        "3.1e2": "int",
        "franklin": "varchar",
    }
    for i in range(0, 10000):
        for k, v in vals.items():
            t0 = time.time()
            if AutoType(k).type != v:
                raise Exception("{} {} {}".format(k, v, AutoType(k).type))
            results.append(time.time() - t0)

    print(1000000 * (sum(results) / len(results)))
