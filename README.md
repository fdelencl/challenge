# Gorgias js2py challenge 

> Please do not make this public - it's been very hard to make this happen. Thank you!

## Intro

One of challenges that we have at Gorgias is managing our Rule system which allows our customers to
automate their work. It's the first thing we built with Gorgias and it is still the core part of our product.

Here's a "real-world" example of a Rule in our interface:

![Rule example](/js2py/challenge/rules.png)

The challenge is to try to replicate a simplified version of the production version by implementing a 
"code transformer" that converts JS code into Python code and runs it against a context of variables.

Example:

```python
context = {'a': 1}
js_code = "a = a + 1"
assert js2py(js_code, context) == {'a': 2}
```

As you can see from the above code, the `js_code` was "executed" and the `a` variable defined in the `context` was 
updated after the function call. You will find the `js2py` function in the `js2py.py` code in the current folder.


### How much of the language needs to be implemented?

We don't need a full-blown js-to-python compiler. We're using only a subset of the language. Specifically:

- if/else conditionals
- Member expressions: `object.property.prop12`
- Boolean expressions: `a && b`
- Boolean operators: `a == b`
- Assignments: `a = 1`

In short the implementation needs to match as much of the language as it's needed to pass the tests from the `test_js2py.py`


### How to setup the dev environment and run the test suite?

```bash
pip install pipenv  # package manager used to install the dependencies

cd challenge_dir
pipenv install # install dependencies
pipenv run pytest -vv  # you should see a lot of failures - the challenge is to fix them :)
```

### What are the constraints?

- Please no clever regular expressions combined with a exec function. They will fail the tests that are not included in this folder.
- No external executables where node.js is called from a separate process for example.
- You don't have to re-implement a lexer/parser **from scratch**, but please don't use `esprima`, `js2py`, `slimit` or libraries similar in functionality, as it would make the task too easy.
- Any other library from pypi/github is allowed, but please don't add too many dependencies.
- The code should be compatible Python3.6
- All tests from `test_js2py.py` should pass.
- Please don't change the filename or the function names already defined in `js2py.py`.


### What is considered a success? 

- There is another test suite that is not included here that we're running on our side to test different edge cases. A good implementation will pass a big part of that test-suite as well.
- Points for reusing libs from the internets. There are a few that can help you a lot, find them. Part of the task is to find the right tool for the job.
- Make sure that when you deliver your code the `Pipfile` and `Pipfile.lock` are up to date with your dependencies using `pipenv update`.
- Follow `import this` - look it up on google if you don't know what `this` is.

Good luck!
