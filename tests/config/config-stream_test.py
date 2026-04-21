class TestErr:  #  =============================================================
    # TODO implement

    def test_disallow_type(_, base_url, config_wf1):
        config = config_wf1.copy()

        config["disallows_streaming"] = 123

        with pytest.raises(TypeError) as exec_info:
            WorkflowApp(None, base_url, config)
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "entry in APP_MODEL_CONFIGS, value of 'disallows_streaming' "
            "must be bool: 123"
        )
