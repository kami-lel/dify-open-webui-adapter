"""
app-get_test.py

Unit Tests (using pytest) for:

BaseDifyApp.get_app_type_and_name()
"""

# pytest fixtres  ##############################################################


# pytest  ######################################################################

# TODO TODO

# err handling  ------------------------------------------------------------

# def test_no_type(_, base_url, workflow_config1, patch_target):
#     config = workflow_config1.copy()
#     mock_resp = Mock()
#     mock_resp.json.return_value = {
#         "name": "Some Names",
#     }

#     with patch(patch_target, return_value=mock_resp):
#         with pytest.raises(ValueError) as exec_info:
#             OWUModel(base_url, config)
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "fail to get App Type from Dify"


# # err handling  ============================================================

# def test_bad_conncetion(_, base_url, workflow_config1, patch_target):
#     config = workflow_config1.copy()

#     with patch(
#         patch_target,
#         side_effect=requests.exceptions.ConnectionError("Bad Connection"),
#     ):
#         with pytest.raises(ConnectionError) as exec_info:
#             OWUModel(base_url, config)
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "fail request to Dify: Bad Connection"
