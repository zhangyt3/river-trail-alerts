import pytest

from unittest.mock import Mock

from Environment import Environment
from frontend.subscribe import handle_subscription_create, render_sign_up_page, render_signed_up_page, create_subscription


def test_create_subscription():
    env_mock = Mock()
    sns_client_mock = Mock()
    sns_client_mock.subscribe.return_value = {'SubscriptionArn': 'test'}
    email = "test@email.com"

    create_subscription(email, env_mock, sns_client_mock)

    env_mock.get.assert_called_once()
    sns_client_mock.subscribe.assert_called_once()

def test_render_signed_up_page_success():
    email = "test@email.com"
    success = True 

    html = render_signed_up_page(email, success)

    assert email in html
    assert "Thanks for subscribing" in html

def test_render_signed_up_page_failed():
    email = "test2@email.com"
    success = False

    html = render_signed_up_page(email, success)

    assert email in html
    assert "Sorry we could not subscribe you" in html

def test_render_sign_up_page():
    env = Environment()
    env.get = Mock(return_value='test-api-endpoint')

    html = render_sign_up_page(env)

    assert 'test-api-endpoint' in html 
