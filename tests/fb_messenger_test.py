import pytest
import os

from unittest.mock import patch

from fb_messenger import verify, form_response_message


def test_verify():
    mode = "subscribe"
    token = "super-secret-token"
    challenge = "test-chalalenge"

    with patch.dict('os.environ', {'PAGE_ACCESS_TOKEN': 'test-page-access-token'}):
        status, returned_challenge = verify(mode, token, challenge)

    assert status == 200
    assert returned_challenge == challenge

def test_form_response_text():
    statuses = [('loc1', 'open'), ('loc2', 'closed')]

    message = form_response_message(statuses)

    assert message == 'loc1: open' + '\n' + 'loc2: closed'

