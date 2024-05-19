# 0x00. AirBnB clone - The console

## Description :house:

**hbnb**: One of the major projects that students in the ALX Software Engineering program are requested to undertake is cloning of the [AirBnB](https://www.airbnb.com/) website.

This happens to be the first web development related project. The project is, however, divided into different sub-projects which include:

- AirBnB Clone - The Console
- AirBnB Clone - Web static
- AirBnB Clone - MySQL
- AirBnB Clone - Deploy static
- AirBnB Clone - Web framework
- AirBnB Clone - RESTful API
- AirBnB Clone - Web Dynamic

As you can see this project is a very comprehensive one but we have just started with the very first one and that's what I want to share with you. Let's get into it then.

## Storage

All the classes are handled by the `Storage` engine in the `FileStorage` Class.

## Environment

 * [pycodestyle (version 2.7.*)](https://pypi.org/project/pycodestyle/)
 * [PEP8](https://pep8.org/)

The project was developed and tested on Ubuntu 20.04 LTS using Python 3.8.3. The developers used a variety of text editors including VIM 8.1.2269, VSCode 1.6.1, and Atom 1.58.0. Git version control system (2.25.1) was used to manage the code.

## Installation

```bash
git clone https://github.com/aysuarex/AirBnB_clone.git
```

change to the `AirBnb` directory and run the command:

```bash
 ./console.py
```

## Execution

In interactive mode

```bash
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb)
(hbnb)
(hbnb) quit
$
```

in Non-interactive mode

```bash
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
```

## Testing

The project leverages a dedicated `tests` folder to store all test definitions.

## Documentation

* Modules:

```python
python3 -c 'print(__import__("my_module").__doc__)'
```

* Classes:

```python
python3 -c 'print(__import__("my_module").MyClass.__doc__)'
```

* Functions (inside and outside a class):

```python
python3 -c 'print(__import__("my_module").my_function.__doc__)'
```

and

```python
python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'
```

## Python Unit Tests

* unittest module
* File extension ``` .py ```
* Files and folders star with ```test_```
* Organization:for ```models/base.py```, unit tests in: ```tests/test_models/test_base.py```
* Execution command: ```python3 -m unittest discover tests```
* or: ```python3 -m unittest tests/test_models/test_base.py```

## run test in interactive mode

```bash
echo "python3 -m unittest discover tests" | bash
```

## run test in non-interactive mode

Discover and execute all tests automatically using the following command:

```bash
python3 -m unittest discover tests
```


## Usage

* Start the console in interactive mode:

```bash
$ ./console.py
(hbnb)
```

* Use help to see the available commands:

```bash
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb)
```

* Quit the console:

```bash
(hbnb) quit
$
```

## Commands

> The commands are displayed in the following format *Command / usage / example with output*

* Create

> *A new object is instantiated from the provided class. The object's ID is printed, and then it's saved to file.json.*

```bash
create <class>

```

```bash
(hbnb) create BaseModel
6cfb47c4-a434-4da7-ac03-2122624c3762
(hbnb)
```

* Show

```bash
show <class> <id>
```

```bash
(hbnb) show BaseModel 6cfb47c4-a434-4da7-ac03-2122624c3762
[BaseModel] (a) [BaseModel] (6cfb47c4-a434-4da7-ac03-2122624c3762) {'id': '6cfb47c4-a434-4da7-ac03-2122624c3762', 'created_at': datetime.datetime(2021, 11, 14, 3, 28, 45, 571360), 'updated_at': datetime.datetime(2021, 11, 14, 3, 28, 45, 571389)}
(hbnb)
```

* Destroy

> *Deletes an instance of a given class with a given ID.*
> *Update the file.json*

```bash
(hbnb) create User
0c98d2b8-7ffa-42b7-8009-d9d54b69a472
(hbnb) destroy User 0c98d2b8-7ffa-42b7-8009-d9d54b69a472
(hbnb) show User 0c98d2b8-7ffa-42b7-8009-d9d54b69a472
** no instance found **
(hbnb)
```

* all

> *Prints all string representation of all instances of a given class.*
> *If no class is passed, all classes are printed.*

```bash
(hbnb) create BaseModel
e45ddda9-eb80-4858-99a9-226d4f08a629
(hbnb) all BaseModel
["[BaseModel] (4c8f7ebc-257f-4ed1-b26b-e7aace459897) [BaseModel] (4c8f7ebc-257f-4ed1-b26b-e7aace459897) {'id': '4c8f7ebc-257f-4ed1-b26b-e7aace459897', 'created_at': datetime.datetime(2021, 11, 13, 22, 19, 19, 447155), 'updated_at': datetime.datetime(2021, 11, 13, 22, 19, 19, 447257), 'name': 'My First Model', 'my_number': 89}"]
["[BaseMode
```

* count

> *Prints the number of instances of a given class.*

```bash
(hbnb) create City
4e01c33e-2564-42c2-b61c-17e512898bad
(hbnb) create City
e952b772-80a5-41e9-b728-6bc4dc5c21b4
(hbnb) count City
2
(hbnb)
```

* update

> *Updates an instance based on the class name, id, and kwargs passed.*
> *Update the file.json*

```bash
(hbnb) create User
1afa163d-486e-467a-8d38-3040afeaa1a1
(hbnb) update User 1afa163d-486e-467a-8d38-3040afeaa1a1 email "aysuarex@gmail.com"
(hbnb) show User 1afa163d-486e-467a-8d38-3040afeaa1a1
[User] (s) [User] (1afa163d-486e-467a-8d38-3040afeaa1a1) {'id': '1afa163d-486e-467a-8d38-3040afeaa1a1', 'created_at': datetime.datetime(2021, 11, 14, 23, 42, 10, 502157), 'updated_at': datetime.datetime(2021, 11, 14, 23, 42, 10, 502186), 'email': 'aysuarex@gmail.com'}
(hbnb)

```
## Authors
<details>
    <summary>Imad Belaallam</summary>
    <ul>
    <li><a href="mailto:imadbelallam@hotmail.com">e-mail</a></li>
    <li><a href="your github link">Github</a></li>
    </ul>
</details>
<details>
    <summary>Youssef Abbya</summary>
    <ul>
    <li><a href="mailto:youssefabbya@gmail.com">e-mail</a></li>
    <li><a href="https://github.com/Youssef-MHD">Github</a></li>
    </ul>
</details>
