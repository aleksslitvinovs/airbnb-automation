# airbnb-automation

## Setup

1. Make sure you have Docker installed and running.
2. Run `./setup.sh` to setup the environment and install dependencies.

## Usage

To run tests using Docker, use the following command:

```bash
docker run --rm -v $(pwd)/temp:/app/temp airbnb-automation
```

To run tests using the local environment, use the following command:

```bash
pytest tests/
```

Options:

- `--suite-timeout`: Maximum time (in seconds) allowed for the entire test suite

- `--headed`: Run tests in headed mode (visible browser). Do not use this option when running in Docker.

## Results

As per the task, results are saved in the `temp` directory. If the directory does not exist, it will be created automatically.

In case of failure, the screenshots will be saved in the `test-results` directory.
