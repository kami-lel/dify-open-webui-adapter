import json


def _convert_entries2list(entries):
    return [
        ("data: " + json.dumps(e)).encode(encoding="utf-8") for e in entries
    ]


def _convert_entries2iter(entries):
    return iter(_convert_entries2list(entries))
