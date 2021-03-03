# SQL Compiler

Our SQL compiler implementation consists of three files:
1. [Lexer](lex.py)
2. [Parser](parse.py)
3. [Main File](sql_compiler.py)

## [Main File](sql_compiler.py)
This is the main file that handles command line arguments and initializes the lexer and parser.

## [Lexer](lex.py)
This file is our lexer implementation. It is responsible for translating the characters and words into tokens (aka lexemes) where each token has a specific token type. A few examples of a token type are:
1. Identifier
2. Keyword
3. Left Parenthesis

It reads character by character and tries to understand what kind of token each word or character is. Then it feeds thos tokens to the parser.

## [Parser](parse.py)
This file is our parser implementation. It receives the tokens from the lexer and tries to figure out if the comply to the SQL grammar rules. It reads the first token to understand the kind of statement and then reads and the rest of the tokens and checks the different grammar rules. If a statement or query is complies to the grammar rules the parser is also responsible for calling the according miniDB function.

## Notes
- The compiler also supports comments (starting with '--').
- It assumes that every keyword is written in capital.
- It assumes that every query ends with a semicolon.
- We have included a setUp() function if you want to avoid writing CREATE and INSERT queries and just test a few SELECT queris. To do that just uncomment the second line inside the query() function in [parse.py](parse.py).

## Quick Start Guide

To use the compiler just type a few SQL commands in a .txt or .sql file and run the following command:
```
python sql_compiler.py test.txt
```

## Example

Let's say we have a file called test.txt with the following SQL queries:

```sql
CREATE DATABASE test;
CREATE TABLE classroom(classroom TEXT, roomNumber INT, capacity INT);
INSERT INTO classroom VALUES('Packard', 101, 500);
INSERT INTO classroom VALUES('Painter', 514, 10);
INSERT INTO classroom VALUES('Packard', 3128, 70);
SELECT * FROM classroom;
SELECT roomNumber FROM classroom WHERE capacity>60;
```

To run the compiler we would do:

![Example](example.png?raw=true)

# miniDB

The miniDB project is a minimal and easy to expand and develop for RMDBS tool, written excusivelly in Python 3. MiniDB's main goal is to provide the user with as much functionality as posssible while being easy to understand and even easier to expand. Thus, miniDB's primary market are students and researchers that want to work with a tool that they can understand through and through, while being able to implement additional features as quickly as possible.

## Installation

Python 3.7 or newer is needed. To download and build the project run:

```bash
git clone https://github.com/DataStories-UniPi/miniDB.git
cd miniDB
pip install -r requirements.txt
```

The last command will install the packages found in [`requirements.txt`](https://github.com/DataStories-UniPi/miniDB/blob/master/requirements.txt). MiniDB is based on the following dependencies:
* `tabulate` (for text formatting)
* `graphviz` (for graph visualizations; optional)
* `matplotlib` (for plotting; optional)

Alternatively, the above dependencies can be installed with the following command:
```python
pip install tabulate graphviz matplotlib
```

Linux users can optionally install the `Graphviz` package to visualize graphs:
```bash
sudo apt-get install graphviz
```
Installation instructions for non-Linux users can be found [here](https://graphviz.org/download/).

## Documentation

The file [documentation.pdf](documentation.pdf) contains a detailed description of the miniDB library (in Greek).

## Loading the [smallRelations database](https://www.db-book.com/db6/lab-dir/sample_tables-dir/index.html)

To create a database containing the smallRelations tables and get an interactive shell, run
``` Python
python -i smallRelationsInsertFile.py
```
You can the access the database through the db object that will be available. For example, you can show the contents of the student table by running the following command:
```python
>> db.show_table('student')
```
The database wil be save with the name `smdb`. You can load the database in a separate Python shell by running the following commands:
```python
>> from database import Database
>> db = Database("smdb", load=True)
```

## Contributors
George S. Theodoropoulos, Yannis Kontoulis, Yannis Theodoridis; Data Science Lab., University of Piraeus.
