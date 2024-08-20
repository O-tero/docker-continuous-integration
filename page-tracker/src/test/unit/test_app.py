import unittest.mock
import pytest
from page_tracker.app import app


@pytest.fixture
def http_client():
    return app.test_client()


@unittest.mock.patch("page_tracker.app.get_redis", autospec=True)
def test_should_call_redis_incr(mock_get_redis, http_client):
    # Given
    mock_redis_instance = mock_get_redis.return_value
    mock_redis_instance.incr.return_value = 5

    # When
    response = http_client.get("/")

    # Then
    assert response.status_code == 200
    assert response.text == "This page has been seen 5 times."
    mock_redis_instance.incr.assert_called_once_with("page_views")
