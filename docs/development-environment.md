# Development environment setup

You want to contribute to Yeti! We're so happy :) Here's the best way to get
you started.


## Clone the code

First of all you'll need to clone Yeti's code if you're going to work on it::

    $ git clone <repo_url>
    $ cd <repo_url>

Now on to installing Yeti's core dependencies.

## Pipenv

We use Pipenv to manage dev and prod dependencies and virtual environments.
You should use it, too!

You can get it through `pip`::

    $ pip install pipenv
    $ pipenv shell --python 3

The second command will automagically create a Python 3 virtual environment
and drop you into a shell that already has it activated

Install dev dependencies:

    $ pipenv install --dev --python 3

This will install all of Yeti's dependencies **plus** its development
dependencies in your new virtual environment.

At this point, you can run the dev API server, although since you have no DB
backend there won't be much to interact with.

## Backend


If you're going to write code for Yeti, you'll need to have an
[ArangoDB](https://www.arangodb.com/) service running on `localhost:8529`.

### macOS

If you're running macOS, odds are you're using [brew](https://brew.sh/)
as your package manager:

    $ brew install arangodb
    $ /usr/local/opt/arangodb/sbin/arangod

The first command will install ArangoDB in your system, the second will run an
instance listening on the default port and default interfaces.


```eval_rst
.. warning::
  Setting up ArangoDB this way is dangerous for production use since it
  is not authenticated whatsoever; but it's more than enough for development
```
### Linux (Ubuntu)

TODO

## Frontend

Setting up the frontend for development is pretty straightforward. Yeti's
frontend is written in [Vue.js](https://vuejs.org/) so you're going to need
`npm` to run it:

```shell
# macOS
$ brew install node

# Ubuntu
$ sudo apt install node
```

To spin up a Vue.js development server (automatically reloads on each file
change, which is quite handy), run these commands from the directory in which
you cloned Yeti::

    $ cd frontend
    $ npm run dev

This will start a webserver listening on `localhost:8080` for connections.

## Documentation

Of course, you'll want to write documentation for all the cool new features
you're about to bring in 😉. We use
[Sphinx](http://www.sphinx-doc.org/en/master/) to generate our documentation,
which is written entirely in markdown.

Once you've updated anything you needed in the `/docs` directory, just run the
following:

```shell
# builds the HTML documentation
$ make html

# opens the file for viewing (MacOS)
$ open _build/html/index.html
```
