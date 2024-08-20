import unittest.mock
import pytest
from page_tracker.app import app
from redis import ConnectionError


@pytest.fixture
def http_client():
    return app.test_client()


@unittest.mock.patch("page_tracker.app.get_redis", autospec=True)
def test_should_call_redis_incr(mock_get_redis, http_client):
    # Given
    mock_redis_instance = mock_get_redis.return_value
    mock_redis_instance.incr.return_value = 5
    mock_redis.return_value.incr.side_effect = ConnectionError

    # When
    response = http_client.get("/")

    # Then
    assert response.status_code == 500
    assert response.text == "Sorry, something went wrong \N{pensive face}"
    mock_redis_instance.incr.assert_called_once_with("page_views")
