# Connector

This document provides instructions on how to set up and run the application.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python
- Make

### Installation

To get a local copy of the code, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/ideepu/connector.git
cd connector
```

Add required environment vars. The application reads from the environment variables exported or from the file `.env`

Set up the local environment for the application. This will create a virtual environment and install the required dependencies:

```bash
make setup
```

To run the application

```bash
make run
```

### Custom run application

The application allows the use of custom arguments that can be passed to it. These arguments can be utilized in the following manner.

**Arguments:**

`--ad_account_id` : The advertisement account ID, which is required to fetch and format the ad details, should be specified for this process. If the advertisement account ID is not provided, the application will automatically select a random account from the available accounts to fetch and format the ad details.

`--start`: The start date in ISO format (YYYY-MM-DD). The application will retrieve the ad details for the target account starting from this date. If not provided, the app will automatically select a random date between 30 and 60 days from today.

`--end`: The end date should be in ISO format (YYYY-MM-DD). The application will retrieve the ad details for the target account up until this date. If not provided, the app will automatically select a random date between the start date and 30 days after the start date.

To see the supported arguments

```bash
poetry run python run.py -h
```

TODO:

- Logging
- Make models strict with proper validations
