import os
from unittest.mock import Mock

import pytest
import requests
from dotenv import load_dotenv

from openweathermap import get_weather_data

load_dotenv()


@pytest.fixture
def api_call_info():
    API_KEY = os.environ["API_KEY"]
    CITY = "London"
    UNITS = "metric"
    return {
        "city": CITY,
        "units": UNITS,
        "URL": f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&units={UNITS}&appid={API_KEY}",
    }


def test_get_weather_data_success(monkeypatch, api_call_info):
    # Mock the requests.get method to return a successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "cod": 200,
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 15.0, "humidity": 60},
        "wind": {"speed": 2.0},
    }
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_response))

    # Call the function and check the result
    result = get_weather_data(api_call_info["URL"])
    assert result == {
        "cod": 200,
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 15.0, "humidity": 60},
        "wind": {"speed": 2.0},
    }


def test_get_weather_data_error(monkeypatch, api_call_info):
    # Mock the requests.get method to return an error response
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"cod": 404, "message": "Failed"}
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_response))

    # Call the function and check the exception
    with pytest.raises(requests.exceptions.HTTPError):
        get_weather_data(api_call_info["URL"])
