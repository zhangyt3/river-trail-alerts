import pytest
import os

from unittest.mock import Mock, patch
from unittest import mock

from notify.notifier import form_email, send_emails


def test_form_email():
    diffs = [
        ('loc1', 'closed', 'open'),
        ('loc2', 'open', 'conditions variable')
    ]
    email_string = form_email(diffs)
    lines = email_string.split('\n')

    assert len(lines) == 2
    assert 'loc1 changed from closed to open' == lines[0]
    assert 'loc2 changed from open to conditions variable' == lines[1]

def test_send_emails():
    diffs = [('Nebraska', 'open', 'closed')]
    sns_client_mock = Mock()
    
    with mock.patch.dict('os.environ', {'EMAIL_SNS_TOPIC_ARN': 'test-arn'}):
        send_emails(sns_client_mock, diffs)
        sns_client_mock.publish.assert_called_once()

