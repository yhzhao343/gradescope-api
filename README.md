# Gradescope API

## Description

This *unofficial* project serves as a library for programmatically interacting with [Gradescope](https://www.gradescope.com/). The primary purpose of this project is to provide students and instructors tools for interacting with Gradescope without having to use the web interface.

For example:

* Students using this project could automatically query information about their courses and assignments to notify them of upcoming deadlines or new assignments.
* Instructors could use this project bulk edit assignment due dates or sync student extensions with an external system.

## Features

Current implemented features include:

* Get all courses for a user
* Get a list of all assignments for a course
* Get all extensions for an assignment in a course
* Add/remove/modify extensions for an assignment in a course
* Add/remove/modify dates for an assignment in a course
* Upload submissions to assignments
* API server to interact with library without Python

## Setup

To use the project you can install the package from PyPI using pip:

```bash
pip install gradescopeapi
```

For additional methods of installation, refer to the [install guide](docs/INSTALL.md)

## Usage

The project is designed to be simple and easy to use. Below is an example of how to use the project to get a list of all courses for a user:

```python
# login and fetch account
connection = GSConnection()
connection.login("email@domain.com", "password")

# get courses
courses = connection.account.get_courses()
```

More examples can be found in the [tests](tests/) directory.

## Testing

For information on how to run your own tests using ```gradescopeapi```, refer to [TESTING.md](docs/TESTING.md)

## Contributing Guidelines

Please refer to the [CONTRIBUTING.md](docs/CONTRIBUTING.md) file for more information on how to contribute to the project.

## Authors

- Susmitha Kusuma
- Berry Liu
- Margaret Jagger
- Calvin Tian
- Kevin Zheng
