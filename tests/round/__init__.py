import json


def _convert_entries2data_lines(entries):
    for e in entries:
        yield ("data: " + json.dumps(e)).encode(encoding="utf-8")
