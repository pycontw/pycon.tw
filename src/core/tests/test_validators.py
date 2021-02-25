import pytest

from django.core.exceptions import ValidationError

from core.validators import EAWMaxLengthValidator


@pytest.fixture
def eaw_max_length():
    return EAWMaxLengthValidator(5)


def test_eaw_max_length_validator_ascii(eaw_max_length):
    eaw_max_length('fooba')


def test_eaw_max_length_validator_ascii_error(eaw_max_length):
    with pytest.raises(ValidationError) as ctx:
        eaw_max_length('foobar')
    assert str(ctx.value) == (
        "['Ensure this value has at most 5 characters (it has 6).']"
    )


def test_eaw_max_length_validator_eaw(eaw_max_length):
    eaw_max_length('一二')
    eaw_max_length('一二3')


def test_eaw_max_length_validator_eaw_error(eaw_max_length):
    with pytest.raises(ValidationError) as ctx:
        eaw_max_length('一二三')
    assert str(ctx.value) == (
        "['Ensure this value has at most 5 characters (it has 6).']"
    )


def test_eaw_max_length_validator_ea_non_wide(eaw_max_length):
    eaw_max_length('ｻﾝｸﾗｽ')


def test_eaw_max_length_validator_ea_non_wide_error(eaw_max_length):
    with pytest.raises(ValidationError) as ctx:
        eaw_max_length('ｻﾝｸﾞﾗｽ')
    assert str(ctx.value) == (
        "['Ensure this value has at most 5 characters (it has 6).']"
    )
