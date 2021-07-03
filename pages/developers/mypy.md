---
layout: page
title: "Static Type Checking"
permalink: /developer/mypy
nav_order: 4
parent: Developer information
---

# Intro to Static Type Checking


## Basics

The most exciting thing happening right now in Python development is static
typing. Since Python 3.0, we've had function annotations, and since 3.6,
variable annotations. In 3.5, we got a "typing" library, which provides tools
to describe types. This is what static type hints look like:

```python
def f(x: int) -> int:
    return x * 5
```

This does nothing at runtime, except store the object. And in the upcoming
Python 3.11 (or 3.7+ with `from __future__ import annotations`), it doesn't
even store the actual object, just the string you type here, so then anything
that can pass the Python parser is allowed here.

It is not useless though! For one, it helps the reader. Knowing the types
expected really gives you a much better idea of what is going on and what you
can do and can't do.

But the key goal is: static type checking! There are a collection of static
type checkers, the most "official" and famous of which is MyPy. You can think
of this as the "compiler" for compiled languages like C++; it checks to make
sure you are not lying about the types. For example, passing in anything that
is not an int to `f` will fail a mypy check, _before you run or deploy any code_.

Your tests cannot test every possible branch, every line of code. MyPy can
(though it doesn't by default, due to gradual typing). You may have code that
runs rarely, that requires remote resources, that is slow, etc. All those can
be checked by MyPy. It also keeps you (too?) truthful in your types.

### Adding types

There are three ways to add types.

1. They can be inline as annotations. Best for Python 3 code, usually.
2. They can be in special "type comments". Required mostly for Python 2 code,
   and still requires the proper imports.
3. They can be in a separate file with the same name but with a `.pyi`
   extension. This is important for type stubs or for cases where you don't
   want to add imports or touch the original code. You can annotate compiled
   files or libraries you don't control this way.

If you have a library you don't control, you can add "type stubs" for it, then
give MyPy your stubs directory. MyPy will pull the types from your stubs. If
you are writing code for a Raspberry Pi, for example, you could add the stubs
for the Pi libraries, and then validate your code, without ever even installing
the Pi-only libraries!

You do not have to add types for every object - most of the time, you just need
it for parameters and returns from functions. When running MyPy, you can use
`reveal_type(...)` to show the inferred type of any object, which is like a
print statement but at type-checking time, or `reveal_locals()` to see all
local types.


### Configuration

By default, MyPy does as little as possible, so that you can add it iteratively
to a code base. By default:
    
* All untyped variables and return values will be Any
* Code inside untyped functions is not checked _at all_

You can add configuration to `pyproject.toml` (and a little bit to the files
themselves), or you can go all the way and pass `--strict`, which will turn on
everything. Try to turn on as much as possible, and increase it until you can
run with full `strict` checking. See the [style page][] for configuration
suggestions.

[style page]: {{ site.baseurl }}{% link pages/developers/style.md %}

For a library to support typing, it has to a) add types using any of the three
methods, and b) add a `py.typed` empty file to indicate that it's okay to look
for types inside it. MyPy also looks in `typeshed`, which is a library full of
type hints for (mostly) the standard library.

Third party libraries that are typed sometimes forget this last step, by the
way!

### Other features

Static typing has some great features worth checking out:

* Unions (New syntax coming in Python 3.10)
* Generic Types (New syntax in Python 3.9)
* Protocols
* Literals
* TypedDict
* Nicer NamedTuple definition (very popular in Python 3 code)
* MyPy validates the Python version you ask for, regardless of what version you
  are running.


## Complete example

### Python 3.6+

Here's the classic syntax, which you need to use if support 3.6+.

```python
from typing import Union, List

# Generic types take bracket arguments
def f(x: int) -> List[int]:
    return list(range(x))

# Unions are a list of types that all could be allowed
def g(x: Union[str, int]) -> None:
    # Type narrowing - Unions get narrowed
    if isinstance(x, str):
        print("string", x.lower())
    else:
        print("int", x)
    
    # Calling x.lower() is invalid here!
```

Run this with `mypy tmp_mypy1.py --strict` and you'll 


### Python 3.7+

```python
from __future__ import annotations

def f(x: int) -> list[int]:
    return list(range(x))

def g(x: str | int) -> None:
    if isinstance(x, str):
        print("string", x.lower())
    else:
        print("int", x)
```

Notice that there are no imports from typing! Note that you cannot use the
"new" syntax in non annotation locations (like unions in `isinstance`) unless
Python supports it at runtime.

You can use the above in earlier Python versions if you use strings.

## Final words

When run alongside a good linter like flake8, this can catch a huge number of
issues before tests or they are discovered in the wild! It also prompts _better
design_, because you are thinking about how types work and interact. It's also
more readable, since if I give you code like this:

```python
def compute(timestamp):
    ...
```

You don't know "what" timestamp is. Is it an int? A float? An object? With
types, you'll know what I was intending to give you. You can use type aliases
to really give expressive names here!
