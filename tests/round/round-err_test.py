# key err  =====================================================================
class TestKeyErrWorkflow:  # ***************************************************

    def test_data_text(
        _, app_wf_skip1, patch_target_post, mock_wf1, stream_entries_wf1
    ):
        app = app_wf_skip1
        patch_target = patch_target_post
        mock_resp = mock_wf1

        entries = [
            *stream_entries_wf1[:-1],
            {
                "event": "text_chunk",
                "workflow_run_id": "b790",
                "task_id": "04db",
                "data": {
                    "from_variable_selector": ["4502", "output"],
                },
            },
        ]
        mock_resp.iter_lines.return_value = _convert_entries2iter(entries)

        with pytest.raises(KeyError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss key in text/event-stream content: 'text'"


class TestKeyErrChatflow:  # ***************************************************

    def test_event(
        _, app_cf_skip1, patch_target_post, mock_cf1, stream_entries_cf1
    ):
        app = app_cf_skip1
        patch_target = patch_target_post
        mock_resp = mock_cf1

        entries = [
            *stream_entries_cf1[:-1],
            {
                "conversation_id": "c0cf",
                "message_id": "ff06",
                "created_at": 1768046345,
                "task_id": "5863",
                "id": "ff06",
                "answer": "FIRST RESPONSE MESSAGE",
                "from_variable_selector": ["llm", "text"],
            },
        ]
        mock_resp.iter_lines.return_value = _convert_entries2iter(entries)

        with pytest.raises(KeyError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss key in text/event-stream content: 'event'"

    def test_answer(
        _, app_cf_skip1, patch_target_post, mock_cf1, stream_entries_cf1
    ):
        app = app_cf_skip1
        patch_target = patch_target_post
        mock_resp = mock_cf1

        entries = [
            *stream_entries_cf1[:-1],
            {
                "event": "message",
                "conversation_id": "c0cf",
                "message_id": "ff06",
                "created_at": 1768046345,
                "task_id": "5863",
                "id": "ff06",
                "from_variable_selector": ["llm", "text"],
            },
        ]
        mock_resp.iter_lines.return_value = _convert_entries2iter(entries)

        with pytest.raises(KeyError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss key in text/event-stream content: 'answer'"
