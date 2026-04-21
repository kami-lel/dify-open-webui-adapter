import json


# mock obj  --------------------------------------------------------------------
def mock_info_wf(info_response_wf1):
    mock_resp = Mock()
    mock_resp.json.return_value = info_response_wf1
    return mock_resp


def mock_info_cf(info_response_cf1):
    mock_resp = Mock()
    mock_resp.json.return_value = info_response_cf1
    return mock_resp


def mock_sefx_info(url, **kwargs):
    pass  # TODO


def _convert_entries2lines(entries):
    return ["data: " + json.dumps(e) for e in entries]


def _convert_lines2list(entries):
    return [
        ll.encode(encoding="utf-8") for ll in _convert_entries2lines(entries)
    ]


def _convert_entries2iter(entries):
    return iter(_convert_lines2list(entries))
