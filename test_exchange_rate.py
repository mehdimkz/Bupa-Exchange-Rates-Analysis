import pytest
import requests
import json
from datetime import date, timedelta, datetime
import time
import pandas as pd
from unittest.mock import patch  # for mocking external calls and dependencies
from diskcache import Cache
import os
import configparser
import matplotlib.pyplot as plt
import sys
from exchange_rate import (
    get_date_range,
    build_request_url,
    fetch_exchange_rate,  
    fetch_exchange_rate_data,  
    calculate_exchange_rate_statistics,
    print_report, 
)

def test_get_date_range():
  # Test getting dates for different numbers of days
  start_date, end_date = get_date_range(7)
  assert end_date == date.today() - timedelta(days=1)
  assert start_date == end_date - timedelta(days=6)

def test_build_request_url():
  base_url = "https://api.example.com"
  api_key = "API_KEY"
  base_currency = "NZD"
  test_date = date(2024, 3, 21)
  expected_url = f"{base_url}/{api_key}/history/{base_currency}/{test_date.strftime('%Y/%m/%d')}"
  assert build_request_url(base_url, api_key, base_currency, test_date) == expected_url

def test_fetch_exchange_rate(monkeypatch):
    """Tests fetch_exchange_rate function with mocked request and response."""
    api_url = 'https://example.com/api/12345/history/AUD/2021/12/31'
    current_date_str = '2021/12/31'
    cache = {}
    expected_nzd_value = 1.2345

    # Mock the requests.get function using monkeypatch.setattr
    def mock_get(url):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {'nzd_value': expected_nzd_value}
        return response

    monkeypatch.setattr('exchange_rate.requests.get', mock_get)

    # Call the function and assert the returned value
    nzd_value = fetch_exchange_rate(api_url, current_date_str, cache)
    assert fetch_exchange_rate(api_url, current_date_str, cache) is None



# Assuming we have pandas (pd) and Cache class imported/defined

@pytest.fixture
def mock_fetch_exchange_rate(monkeypatch):
    """Mocks the fetch_exchange_rate function to return a predictable value."""
    def mock_fetch(api_url, date_str, cache):
        return 1.23  # Replace with a known value for testing

    monkeypatch.setattr('exchange_rate', 'fetch_exchange_rate', mock_fetch)

def test_fetch_exchange_rate_data():
    """Tests basic functionality of fetch_exchange_rate_data."""

    # Mock external dependencies 
    def mock_fetch_exchange_rate(api_url, date_str, cache):
        # Simulate successful data retrieval for a single date
        return 1.23  

    def mock_build_request_url(base_url, api_key, base_currency, current_date):
        return 'https://api.example.com/data'  # Replace with a dummy URL

    # Set up test data
    start_date = pd.to_datetime('2024-05-01')
    end_date = pd.to_datetime('2024-05-01')
    base_currency = 'AUD'
    api_key = 'your_api_key'
    base_url = 'https://api.example.com'

    # Patch dependencies 
    with patch('exchange_rate.fetch_exchange_rate', side_effect=mock_fetch_exchange_rate):
        with patch('exchange_rate.build_request_url', side_effect=mock_build_request_url):
            df = fetch_exchange_rate_data(start_date, end_date, base_currency, api_key, base_url)

    # Assertions
    assert len(df) == 1  # Expect one row for a single date
    assert df.loc[0, 'Date'] == start_date.strftime('%Y/%m/%d')
    assert df.loc[0, 'AUD_NZD_ExRate'] == 1.23


def test_calculate_exchange_rate_statistics_empty_df():
  """Tests calculate_exchange_rate_statistics with an empty DataFrame."""
  empty_df = pd.DataFrame(columns=['Date', 'AUD_NZD_ExRate'])
  best_rate, worst_rate, average_rate = calculate_exchange_rate_statistics(empty_df)
  assert pd.isna(best_rate)
  assert pd.isna(worst_rate)
  assert pd.isna(average_rate)  

def test_calculate_exchange_rate_statistics_single_record():
  """Tests calculate_exchange_rate_statistics with a single record DataFrame."""
  data = {'Date': ['2024-05-01'], 'AUD_NZD_ExRate': [1.1234]}
  df = pd.DataFrame(data)
  best_rate, worst_rate, average_rate = calculate_exchange_rate_statistics(df)
  assert best_rate == 1.1234
  assert worst_rate == 1.1234
  assert average_rate == 1.1234   

def test_print_report_empty_df():
  """Tests print_report with an empty DataFrame."""
  empty_df = pd.DataFrame(columns=['Date', 'AUD_NZD_ExRate'])
  start_date_str = "2024-05-01"
  end_date_str = "2024-05-01"
  print_report(empty_df, start_date_str, end_date_str, None, None, None)


def test_print_report_basic():
  """Tests print_report with a DataFrame containing data."""
  data = {'Date': ['2024-05-01', '2024-05-02'], 'AUD_NZD_ExRate': [1.1234, 1.1156]}
  df = pd.DataFrame(data)
  start_date_str = '2024-05-01'
  end_date_str = '2024-05-02'
  best_rate = 1.1234
  worst_rate = 1.1156
  average_rate = 1.1195

  # Capture the output using a StringIO object
  from io import StringIO
  captured_output = StringIO()
  sys.stdout = captured_output

  print_report(df, start_date_str, end_date_str, best_rate, worst_rate, average_rate)

  # Reset stdout
  sys.stdout = sys.__stdout__

  # Assert the captured output contains expected elements
  assert 'Report:' in captured_output.getvalue()
  assert f'Date Range: {start_date_str} - {end_date_str}' in captured_output.getvalue()
  assert f'Number of days: {len(df)}' in captured_output.getvalue()

