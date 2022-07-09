from hyperfocus.utils import un_camel_case


def test_un_camel_case():
    camel_case_str = "CamelCase"

    assert un_camel_case(camel_case_str) == "camel case"
