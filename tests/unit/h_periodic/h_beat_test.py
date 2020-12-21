import pytest

from h_periodic.h_beat import asbool


@pytest.mark.parametrize("uppercase", [True, False])
@pytest.mark.parametrize("prefix", ["", " ", "   "])
@pytest.mark.parametrize("suffix", ["", " ", "   "])
@pytest.mark.parametrize(
    "s,expected_output",
    [
        ("t", True),
        ("true", True),
        ("y", True),
        ("yes", True),
        ("on", True),
        ("1", True),
        ("", False),
        ("f", False),
        ("false", False),
        ("n", False),
        ("no", False),
        ("off", False),
        ("0", False),
    ],
)
def test_asbool(s, expected_output, uppercase, prefix, suffix):
    if uppercase:
        s = s.upper()
    s = prefix + s + suffix

    assert asbool(s) == expected_output


def test_asbool_returns_falsey_for_None():
    assert not asbool(None)
