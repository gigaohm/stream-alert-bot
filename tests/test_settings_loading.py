import os.path
import pytest

from sab import helpers


MISC_PATH = "/".join([os.path.abspath("."),
                     "tests/misc"])


def test_load_nonexisting_file():
    with pytest.raises(SystemExit) as run:
        assert helpers.load_yaml("null.yaml")
    assert run.value.code == 2


def test_yaml_wrong_syntax():
    print(MISC_PATH)
    with pytest.raises(SystemExit) as run:
        assert helpers.load_yaml("/".join([MISC_PATH, "wrong_syntax.yaml"]))
    assert run.value.code == 5
