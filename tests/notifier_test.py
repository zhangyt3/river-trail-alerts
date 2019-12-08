import pytest

from notify.notifier import form_email


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
    
