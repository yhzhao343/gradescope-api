# Example showing how to import different components of the package and use them in the main function

from sylveon._hello._greeting import hello_world
from sylveon.string_length.find_length import find_length
from sylveon._classes._connection import GSConnection
from dotenv import load_dotenv
import os


def main():
    greeting = hello_world()
    print(greeting)
    length_str = find_length(greeting)
    print(f"Length of string {greeting} is {length_str}")

    connection = GSConnection()

    # load .env file
    load_dotenv()

    # login
    connection.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    account = connection.account

    # get courses
    courses = account.get_courses()

    print(courses)


if __name__ == "__main__":
    main()
