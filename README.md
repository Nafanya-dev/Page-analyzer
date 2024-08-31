### Hexlet tests and linter status:
[![Actions Status](https://github.com/Nafanya-dev/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Nafanya-dev/python-project-83/actions)

<a href="https://codeclimate.com/github/Nafanya-dev/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/a28470cbd604686f3085/maintainability" /></a>

## About

Page Analyzer is a full-featured application based on the Flask framework that analyzes specified pages for SEO suitability.

In this project the Bootstrap 5 framework along with Jinja2 template engine are used. The frontend is rendered on the backend. This means that the page is built by the Jinja2 backend, which returns prepared HTML. And this HTML is rendered by the server.

PostgreSQL is used as the object-relational database system with Psycopg library to work with PostgreSQL directly from Python.

[Domain](https://python-project-83-a43e.onrender.com)

---

## Installation

### Prerequisites

### Python

Before installing the package make sure you have Python version 3.8 or higher installed:

```bash
>> python --version
Python 3.10+
```

#### Poetry

The project uses the Poetry dependency manager. To install Poetry use its [official instruction](https://python-poetry.org/docs/#installation).

#### PostgreSQL

As database the PostgreSQL database system is being used. You need to install it first. You can download the ready-to-use package from [official website](https://www.postgresql.org/download/) or use apt:
```bash
>> sudo apt update
>> sudo apt install postgresql
```

### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
>> git clone https://github.com/Nafanya-dev/Page-analyzer.git && cd Page-analyzer
```

Then you have to install all necessary dependencies:

```bash
>> make install
```

Create .env file in the root folder and add following variables:
```
DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
SECRET_KEY = '{your secret key}'
```
Run commands from `database.sql` to create the required tables.

---

## Usage

Start the gunicorn Flask server by running:
```bash
make start
```
By default, the server will be available at http://0.0.0.0:8000.

_It is also possible to start it local in development mode with debugger active using:_
```bash
make dev
```


To add a new site, enter its address into the form on the home page. The specified address will be validated and then added to the database.

After the site is added, you can start checking it. A button appears on the page of a particular site, and clicking on it creates an entry in the validation table.

You can see all added URLs on the `/urls` page.
