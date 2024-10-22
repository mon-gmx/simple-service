from unittest.mock import Mock

from services import get_random


def test_get_random_success(mock_remote_get_random) -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"random_data": "SOMETHING"}

    mock_remote_get_random.return_value = mock_response
    result = get_random(remote_url="http://1.1.1.1/data")

    mock_remote_get_random.assert_called_once_with("http://1.1.1.1/data")
    assert result == {"random_data": "SOMETHING"}


def test_get_random_failure(mock_remote_get_random) -> None:
    mock_response = Mock()
    mock_response.status_code = 404

    mock_remote_get_random.return_value = mock_response
    result = get_random(remote_url="http://1.1.1.1/data")

    mock_remote_get_random.assert_called_once_with("http://1.1.1.1/data")

    assert (
        len(result) == 36
    )  # uuid4 is 36 char long, this could be tested using ValueError
