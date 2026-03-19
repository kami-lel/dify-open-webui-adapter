"""
round-err_test.py

Unit Tests (using pytest) for:

errs handling in _StreamingConversationRound.__next__()
"""

# pytest fixtures  #############################################################

# pytest  ######################################################################

# FIXME update tests


class TestExhaust:  # ==========================================================
    pass


#     def test_workflow1(_):
#         data_dicts = WORKFLOW_DATA1[:2]
#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts(data_dicts)
#         )

#         with pytest.raises(ValueError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert (
#             opt
#             == "exhaust text/event-stream "
#             "but detect no events indicating finishing"
#         )

#     def test_chatflow1(_):
#         data_dicts = CHATFLOW_DATA1[:2]
#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts(data_dicts)
#         )

#         with pytest.raises(ValueError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert (
#             opt
#             == "exhaust text/event-stream "
#             "but detect no events indicating finishing"
#         )


class TestUnicode:  # ==========================================================
    pass


#     def test_workflow1(_):
#         lines = convert_lines_from_data_dicts(WORKFLOW_DATA1)
#         bytes_obj = [bytearray(line, "utf_16") for line in lines]
#         text_streams = iter(bytes_obj)

#         with pytest.raises(UnicodeDecodeError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert (
#             opt
#             == "fail to decode text/event-stream: "
#             "'utf-8' codec can't decode byte 0xff in position 0: "
#             "invalid start byte"
#         )

#     def test_chatflow1(_):
#         lines = convert_lines_from_data_dicts(CHATFLOW_DATA1)
#         bytes_obj = [bytearray(line, "utf_16") for line in lines]
#         text_streams = iter(bytes_obj)

#         with pytest.raises(UnicodeDecodeError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert (
#             opt
#             == "fail to decode text/event-stream: "
#             "'utf-8' codec can't decode byte 0xff in position 0: "
#             "invalid start byte"
#         )


class TestJSONDecode:  # =======================================================
    pass


#     def test1(_):
#         bad_json = 'data: {"text": "value'
#         text_streams = convert_bytes_generator_from_lines([bad_json])

#         with pytest.raises(JSONDecodeError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt.startswith("fail to parse text/event-stream as JSON")


class TestKeyErrWorkflow:  # ===================================================
    pass


#     def test_event(_):
#         data = {
#             "workflow_run_id": "b790",
#             "task_id": "04db",
#             "data": {
#                 "text": "FIRST RESPONSE MESSAGE",
#                 "from_variable_selector": ["4502", "output"],
#             },
#         }
#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'event'"

#     def test_data(_):
#         data = {
#             "event": "text_chunk",
#             "workflow_run_id": "b790",
#             "task_id": "04db",
#         }
#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'data'"

#     def test_data_text(_):
#         data = {
#             "event": "text_chunk",
#             "workflow_run_id": "b790",
#             "task_id": "04db",
#             "data": {
#                 "from_variable_selector": ["4502", "output"],
#             },
#         }
#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'text'"


class TestKeyErrChatflow:  # ===================================================
    pass


#     def test_event(_):
#         data = {
#             "conversation_id": "c0cf",
#             "message_id": "ff06",
#             "created_at": 1768046345,
#             "task_id": "5863",
#             "id": "ff06",
#             "answer": "FIRST RESPONSE MESSAGE",
#             "from_variable_selector": ["llm", "text"],
#         }

#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'event'"

#     def test_answer(_):
#         data = {
#             "event": "message",
#             "conversation_id": "c0cf",
#             "message_id": "ff06",
#             "created_at": 1768046345,
#             "task_id": "5863",
#             "id": "ff06",
#             "from_variable_selector": ["llm", "text"],
#         }

#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'answer'"
