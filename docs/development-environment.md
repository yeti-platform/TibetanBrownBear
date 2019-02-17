# Development environment setup

You want to contribute to Yeti! We're so happy :) Here's the best way to get
you started.

## Fork the repo and clone the code

We recommend you fork any repo you're thinking of contributing to. This will create a new `github.com/<YOUR USERNAME>/yeti-platform` repo on which you can push changes and from which you can submit pull-requests.

After forking the repo, just clone it::

    $ git clone https://github.com/<YOUR USERNAME>/yeti-platform
    $ cd yeti-platform

## Install dependencies

We use Pipenv to manage dependencies and virtual environments.
You should use it, too!

You can get it through `pip`::

    $ pip install pipenv
    $ pipenv shell --python 3

The second command will automagically create a Python 3 virtual environment
and drop you into a shell that already has it activated

Install dev dependencies:

    $ pipenv install --dev

This will install all of Yeti's dependencies **plus** its development
dependencies in your new virtual environment.

## Set up your database backend

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
### Linux (Ubuntu 16.04)

Add the ArangoDB repo key to your install, update your packages and install everything as usual.

    $ wget https://www.arangodb.com/repositories/arangodb3/xUbuntu_16.04/Release.key
    $ sudo apt-key add Release.key
    $ sudo apt-add-repository 'deb https://www.arangodb.com/repositories/arangodb3/xUbuntu_16.04/ /'
    $ sudo apt-get update -y && sudo apt-get install arangodb3 --allow-unauthenticated

```eval_rst
.. warning::
  Setting up ArangoDB this way is dangerous for production use since it
  is not authenticated whatsoever; but it's more than enough for development
```

## Import demo data

If you're about to develop a new feature for Yeti, it might be useful to populate your database with some data.

### Import a TAXII feed

Start by importing one of MITRE's TAXIi feeds. ATT&CK is a good start:

```
$ yeticli taxii-import --server_url https://cti-taxii.mitre.org/taxii/
https://cti-taxii.mitre.org/taxii/ has 3 collections:
[0] Enterprise ATT&CK: 95ecc380-afe9-11e4-9b6c-751b66dd541e
[1] PRE-ATT&CK: 062767bd-02d2-4b72-84ba-56caef0f8658
[2] Mobile ATT&CK: 2f669986-b40b-4423-b720-4396ca6a462b
Pick one: 0
Importing data from collection at: https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/
Fetching attack-pattern
[...]
```

### Add users to the database

You'll also want to add users to your database:

    $ yetictl add-user admin@yourorg.com --admin

or, if you haven't installed the scripts:

    $ python ctl/yetictl.py add-user admin@yourorg.com --admin

And follow the on-screen prompts.

## Running the frontend

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

    $ cd yeti/web/frontend
    $ npm run dev

This will build and start a webserver listening on `localhost:8080` for connections.

## Building documentation

Of course, you'll want to write documentation for all the cool new features
you're about to bring in 😉. We use
[Sphinx](http://www.sphinx-doc.org/en/master/) to generate our documentation,
which is written Markdown (with some reST directives here and there).

Once you've updated anything you needed in the `/docs` directory, just run the
following:

```shell
# get into the right directory
$ cd docs

# builds the HTML documentation
$ make html

# opens the file for viewing (MacOS)
$ open _build/html/index.html
```
