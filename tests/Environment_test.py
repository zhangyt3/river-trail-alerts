import pytest

from unittest.mock import Mock, patch

from Environment import Environment


def test_get():
    env = Environment()
    with patch.dict('os.environ', {'TEST_ENV_VAR': 'TEST_VALUE'}):
        res = env.get('TEST_ENV_VAR')
        assert res == 'TEST_VALUE'

def test_get_expect_error():
    env = Environment()

    with pytest.raises(KeyError):
        res = env.get('NON_EXISTENT_ENVIRONMENT_VARIABLE_SAOJD)QJD#(*@EJJ')

