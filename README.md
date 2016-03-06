# Baseships Game

Classic battleship game as a web application written in Python and Django. Project was developed and tested on Linux Ubuntu 14.04.

## Installation

- Clone this repo:

    `$ git clone https://github.com/9dev/baseships`

- Make sure you have `fabric` and `virtualenv` installed on your computer:

    `$ sudo pip install fabric virtualenv`

- Execute the following command inside the main directory:

    `$ fab install`

## Playing

- Run the game:

    `$ fab runserver`

- Navigate to `http://127.0.0.1:8000`.

- When asked to log in, use credentials `admin : admin`.

## Tests

Project comes with a full suite of functional tests. You can run all of them by executing:

`$ fab test`

Note: Tests come with a ChromeDriver binary for 64-bit Linux, but you can easily replace it with any other version.

## Meaning of colors

- SILVER - undiscovered
- WHITE - missed
- GREEN - filled (with your ship)
- RED - hit
- BLUE - sunk
