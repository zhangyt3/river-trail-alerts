import pytest
import os

from unittest.mock import patch

from fb_messenger import verify


def test_verify():
    mode = "subscribe"
    token = "super-secret-token"
    challenge = "test-chalalenge"

    with patch.dict('os.environ', {'PAGE_ACCESS_TOKEN': 'test-page-access-token'}):
        status, returned_challenge = verify(mode, token, challenge)

    assert status == 200
    assert returned_challenge == challenge

