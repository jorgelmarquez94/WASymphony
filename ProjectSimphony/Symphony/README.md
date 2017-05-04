[![Stories in Ready](https://badge.waffle.io/AliGhahraei/Project-Simphony.png?label=ready&title=Ready)](https://waffle.io/AliGhahraei/Project-Simphony)
# Project-Symphony
A language for music lovers

## Installation
What follows is the recommended installation method.

1. Install Python3, pip and virtualenv using your preferred method. Just make sure you install a recent version.

1. Create an environment inside the project directory:

        $ virtualenv venv
  
1. Now activate it:

        $ source venv/bin/activate
  
1. And install our requirements:

        $ pip install -r requirements.txt

## Tests
Just run the desired test using unittest (after you activate your venv!).

Example:

    $ source venv/bin/activate    # if you still haven't done it
    $ python -m unittest lexer_parser_test.py
