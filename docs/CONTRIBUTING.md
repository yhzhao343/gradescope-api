# Contributing Guidelines

## Setup

Clone the repository. This project currently uses [PDM](https://pdm-project.org/en/latest/) for dependency management. If you do not plan to make any changes to the dependencies, you can use `pip` to install the dependencies instead.

```bash
# PDM
pdm install -d
```

```bash
# pip
pip install -r requirements.txt
```

## Tests

Tests are performed using real Gradescope accounts to interact with the Gradescope server. As such, valid Gradescope accounts and courses are required to run the tests.

### Environment

Create an `.env` file in the root directory of the project with the following environment variables:

```
GRADESCOPE_CI_STUDENT_EMAIL
GRADESCOPE_CI_STUDENT_PASSWORD
GRADESCOPE_CI_INSTRUCTOR_EMAIL
GRADESCOPE_CI_INSTRUCTOR_PASSWORD
```

### Running tests locally

Tests can be run locally using `pytest`. A PDM script is also provided to run the tests.

```bash
pytest tests
# or
pdm run test
```

### CI

Tests are run automatically using GitHub Actions.

### Running CI locally

Install [act](https://github.com/nektos/act)

From the root of the repository, run the following command and pass in the `.env` file for Gradescope test account credentials:

```bash
act --secret-file .env
```
