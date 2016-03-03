### Deployment Instructions

1. Start new machine - `docker-machine create -d virtualbox dev`
1. Build images - `docker-compose build`
1. Start services - `docker-compose up -d`
1. Apply migrations - `docker-compose run web /usr/local/bin/python manage.py migrate`
1. Load fixtures - `docker-compose run -d web /usr/local/bin/python manage.py loaddata dump.json`
1. Grab IP - `docker-machine ip dev` - and view in your browser  

> More: https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/

# Python Coding Guidelines

`import this`  # Zen of Python

- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.
- Flat is better than nested.
- Sparse is better than dense.
- Readability counts.
- Special cases aren't special enough to break the rules.
- Although practicality beats purity.
- Errors should never pass silently.
- Unless explicitly silenced.
- In the face of ambiguity, refuse the temptation to guess.
- There should be one—and preferably only one—obvious way to do it.
- Although that way may not be obvious at first unless you're Dutch.
- Now is better than never.
- Although never is often better than right now.
- If the implementation is hard to explain, it's a bad idea.
- If the implementation is easy to explain, it may be a good idea.
- Namespaces are one honking great idea—let's do more of those!


### Whitespaces:
- 4 spaces per indentation level.
- Never mix tabs and spaces, spaces are preferred
- One blank line between functions.
- Two blank lines between classes.
- Add a space after `,` in dicts, lists, tuples, & argument lists, and after `:` in dicts, but not before.
- Put spaces around assignments & comparisons (except in argument lists).
- No spaces just inside parentheses or just before argument lists.

### Naming:
- __joined_lower__ for functions, methods, attributes
- __ALL_CAPS__ for constants
- __StudlyCaps__ for classes
- Attributes: __interface__, ___internal__, ____private__  (don't overuse ____private__, it's not really private)

Multiple statements on one line are a cardinal sin. In Python, readability counts.

### Docstrings and comments:
- Docstrings -> How to use code (explains how to use code, and are for the users of your code)
- Comments -> Why (rationale) & how code works (explains why, and are for the maintainers of your code.)

#### Idioms:
- Always use an object's capabilities instead of its type (you shouldn't care whether an object is a particular type as long as it supports a particular interface)
- While lots of kinds of black magic are possible in Python, the most straight forward and explicit method is preferred (`return {'x': x, 'y': y}` vs. `return dict(**locals())`)
- Default parameter values should never be mutable objects (wrong: `def bad_append(item, list=[])`)
- String concatenation: Use `result = ''.join(string_list)` and never `for s in string_list: result += s`
- Use tuples to unpack data. Use `(animal, name, age) = ['dog', 'Fido', 10]` instead of accesing list items by index.
- Use '__' to ignore unpacked data. Use `animal, __, __ = ['dog', 'Fido', 10]` when just the first item is needed.
- Use `in` wherever possible (`for key in d` instead of `for key in d.keys()`)
- Use `if not x` instead of `if x == 0` or `if x == ""` or `if x == None` or `if x == False`
- Use string methods rather than the string module: `s.startswith('abc')` instead of `startswith(s, 'abc')`
- Use `while True:` for infinite loops, or to always execute the loop body at least once
- Catch errors rather than avoiding them to avoid cluttering your code with special cases ('easier to ask forgiveness than permission')
- Catch only the appropriate errors (generic exception catching should be used rarely and carefully)
- Swap values without using temporary variables (`a, b = b, a`)
- Use `zip` to get a list's (or any sequence's) items with their indices
- Use `for idx, item in enumerate(list):` to loop over a list and having access to both index and data
- Use `sorted(list, key=func)` to sort a list by the result of the 'key' function for each item in the list
- Use the new style string formatting: `'{} {}'.format('one', 'two')` (https://pyformat.info/)
- Use list comprehensions instead of a simple `for` but remember that readability counts
- Use generator expressions instead of list comprehensions when the computed list is just an indermediate step
- Use the simplest option that could possibly work. Don't use a regular expression if you just want to see if a string starts with a particular substring: use `.startswith` instead. Don't use `.index` if you just want to see if a string contains a particular letter: use `in` instead.
- Don’t use the `dictionary.has_key()` method. Instead, use `x in dictionary` syntax, or pass a default argument to `dictionary.get()`.
- Use Context Managers to ensure resources are properly managed.
- Use the `with open(path_to_file, access_mode) as file_handle:` syntax to read from files. This will automatically close files for you.


### Anti-Idioms:
- `from module import *` You should always import just what you need
- `except Exception:` Catching any raised exception will hinder the debugging process if something unexpected happens
