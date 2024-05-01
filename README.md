# Data Engineering Challenge: AUD/NZD Exchange Rates Analysis

Data Engineering Challenge: AUD/NZD Exchange Rates Analysis


## Table of Contents

- [Data Engineering Challenge: AUD/NZD Exchange Rates Analysis](#data-engineering-challenge-audnzd-exchange-rates-analysis)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Setup](#setup)
    - [Prerequisites:](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Approach](#approach)
      - [1. Data Acquisition:](#1-data-acquisition)
      - [2. Data Preprocessing:](#2-data-preprocessing)
      - [3. Data Analysis:](#3-data-analysis)
      - [4. Output:](#4-output)
      - [5. Script Orchestration:](#5-script-orchestration)
  - [Libraries and Tools](#libraries-and-tools)
  - [Testing](#testing)
    - [Key Design Principles](#key-design-principles)
  - [Contact](#contact)

## Project Overview

This project analyzes historical exchange rates between the Australian Dollar (AUD) and the New Zealand Dollar (NZD) for the past 30 days. It retrieves data from the Exchange Rates API (https://www.exchangerate-api.com/), performs data processing, calculates key statistics, and visualizes the results.
## Setup
### Prerequisites:

- Python 3.x
and the following libraries to be installed:

- `requests`
- `datetime`
- `pandas`
- `diskcache`
- `matplotlib`
- `pytest nbval` (optional, for testing)

### Installation

1. Clone the repository:

  ```bash
   git clone https://github.com/mehdimkz/Bupa-Exchange-Rates-Analysis.git
```
2. You can install the dependencies by running the following commands:

 ```bash
 pip install requests datetime pandas diskcache matplotlib pytest nbval
 ```
3. Configure the API key:

    Create a config.ini file in the root directory of the project. Add the following contents to the config.ini file (In our project, Its already created and saved in repository): 
```bash
[API]
API_KEY = your-api-key
``` 
## Usage

To run the script, follow one of the methods below:
 1. Command Line:
Open the command line interface and navigate to the directory where the script `exchange_rate.py` is located. Then execute the following command:
```
python exchange_rate.py
```
2. Jupyter Notebook:
Open Jupyter Notebook and navigate to the directory where the `exchange_rate.ipynb` file is located. Open the file and run the cells inside the notebook to execute the script.

This will generate the following outputs:

1. A CSV file named "exchange_rate_data.csv" containing the exchange rate data for the specified period. The best, worst, and average exchange rates, along with the start and end dates of the analysis also will be added to the end of CSV sheet.

2. A line plot visualizing the exchange rate trend over time.
3. A report within the console summarizing the best, worst, and average exchange rates, along with the start and end dates of the analysis.

## Approach

The script follows these key steps:

#### 1. Data Acquisition:

- **Function:** `get_date_range(num_days)`
This function calculates the desired start and end dates based on the specified number of days (num_days).
- **Function:** `build_request_url(base_url, api_key, base_currency, date_obj)`
This function builds the URL for the API request, including the base URL, API key, base currency (base_currency), and the desired date (date_obj).
- **Function:** `fetch_exchange_rate(api_url, current_date_str, cache)`
This function fetches the exchange rate for a specific date using the provided API URL (api_url), date string (current_date_str), and a caching mechanism (cache). It utilizes caching to avoid redundant API calls for previously retrieved data.
#### 2. Data Preprocessing:

- **Function:** `fetch_exchange_rate_data(start_date, end_date, base_currency, api_key, base_url)`
This function retrieves the exchange rate data for the entire date range specified by start_date and end_date. It iterates through each date, builds the corresponding API URL using the build_request_url function, and fetches the exchange rate using the fetch_exchange_rate function. The retrieved data is stored in a pandas DataFrame.
#### 3. Data Analysis:

- **Function:** `calculate_exchange_rate_statistics(df)`
This function calculates the best, worst, and average exchange rates from the pandas DataFrame (df) containing the exchange rate data.
- **Function:** `plot_exchange_rate_data(df)`
This function generates a line plot visualizing the exchange rate trend over time using the data in the DataFrame (df).
#### 4. Output:

- **Function:** `print_report(df, start_date_str, end_date_str, best_rate, worst_rate, average_rate)`
The Function displays the DataFrame along with a summary report containing the start and end dates, number of days, and calculated statistics.

#### 5. Script Orchestration:
- **Function:**
`main()`, It defines the overall flow of the script by sequentially calling functions like:
`get_api_key`: Retrieves the API key from the configuration file. \
`fetch_exchange_rate_data`: Fetches exchange rate data for the specified date range. \
`calculate_exchange_rate_statistics`: Calculates key statistics from the exchange rate data. \
`print_report`: Prints the report summarizing the analysis results. \
`plot_exchange_rate_data`: Generates the exchange rate plot. \
Additional functions for saving data to CSV files.

***By encapsulating the core functionality within the `main` function, I improve code organization and maintainability.***

## Libraries and Tools
+ requests: Makes HTTP requests to the API.
+ json: Parses JSON responses from the API.
+ datetime: Handles date and time calculations.
+ pandas: Used for data manipulation and analysis.
+ diskcache: Implements caching for API calls.
+ matplotlib: Creates the exchange rate plot.
+ configparser: Parses API key from a configuration file.


## Testing
 The code is designed with modularity and clarity for easy testing. This project utilises the `pytest` framework for unit testing. All tests are located in the `test_exchange_rate.py` file.

  **Running Tests:**
To run the tests,first we need to install pytest as below and then we can execute the following command from our terminal within the project directory:


```bash
1. pip install pytest
2. pytest test_exchange_rate.py
```
Here's a breakdown of the testing approach:

**Test Coverage:**

Each function within the `exchange_rate.py` module has a dedicated test case in `test_exchange_rate.py`.
These tests isolate the behavior of each function, verifying its correctness under various scenarios.
- **Mocking External Calls:**
Functions that interact with external resources (e.g., API requests) utilize the `monkeypatch` fixture from `unittest.mock`.
This allows mocking external dependencies like the API response, ensuring tests are independent of external factors.

**Specific examples:**
`test_get_date_range`: Verifies the calculation of the desired date range based on the specified number of days.
`test_build_request_url`: Ensures the correct construction of the API request URL with the base URL, API key, base currency, and target date
`test_fetch_exchange_rate`: Mocks the requests.get function to simulate successful and unsuccessful API responses.
`test_fetch_exchange_rate_data`: Mocks the fetch_exchange_rate function to ensure that fetch_exchange_rate_data can handle a single date and populate the DataFrame correctly, other scenarios also can be added.
`test_calculate_exchange_rate_statistics`: Tests the function with empty and single-record DataFrames, verifying correct calculations.
`test_print_report`: Tests the report generation with both empty and populated DataFrames, asserting the presence of expected information.

### Key Design Principles

+ **Separation of Concerns:** Each function has a clear purpose and avoids mixing responsibilities.
+ **Modularity:** Functions are independent units, promoting maintainability and reusability.
+ **Data Flow:** The code follows a logical flow from data retrieval, processing, analysis, and output generation.
+ **Caching:** fetch_exchange_rate utilizes caching to optimize API calls.
+ **Configuration:** API key retrieval is separated from the main logic using get_api_key.

This architecture promotes code clarity, maintainability, and testability. Each component can be easily understood, modified, or tested independently.

## Contact
Feel free to reach out if you have any questions or suggestions:

* Email: me.malekzadeh@gmail.com
