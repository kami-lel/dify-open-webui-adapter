# TODO


class TestErr:

    def test_empty(_, base_url):
        ipt = []

        with pytest.raises(ValueError) as exec_info:
            Pipe(
                app_model_configs_override=ipt,
                base_url_override=base_url,
                skip_get_app_type_and_name=True,
            )

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS must contain at least one App/Model"

    def test_bad_type1(_, configs_mux, base_url):
        ipt = configs_mux.copy()
        ipt.append(123)

        with pytest.raises(ValueError) as exec_info:
            Pipe(
                app_model_configs_override=ipt,
                base_url_override=base_url,
                skip_get_app_type_and_name=True,
            )

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS must contains only dicts: (123,)"

    def test_bad_type2(_, configs_mux, base_url):
        ipt = configs_mux.copy()
        ipt.append([1, 2, 3])
        ipt.append("abc")

        with pytest.raises(ValueError) as exec_info:
            Pipe(
                app_model_configs_override=ipt,
                base_url_override=base_url,
                skip_get_app_type_and_name=True,
            )

        msg = str(exec_info.value)
        print(msg)

        assert (
            msg
            == "APP_MODEL_CONFIGS must contains only dicts: ([1, 2, 3], 'abc')"
        )
