# RESTful API

Yeti is built around a restful HTTP API. Everything you can do from the web
frontend you can also do through a couple of well-formed `curl` or `HTTPie`
requests.

## Installing HTTPie

[HTTPie](https://httpie.org/) is a tiny CLI utility that we'll use instead of
`curl`. It supports easy sending of data and JSON requests, and nicely displays
JSON output::

    # macOS
    $ brew install httpie

## Creating new objects

TODO

## Searching and filtering

### `/api/{entities,indicators}/filter/`

You can search for `entities` or `indicators` by providing
`name` and `type` parameters.

**Method and endpoint**

* `POST /api/{entities,indicators}/filter/`

**JSON body**

* `name`: String, name to filter on (emtpy string to list all items)
* `type`: String, type to filter on (these are STIX 2 types)

**Response**

List of JSON-encoded entities / indicators. Take a look at the [STIX 2 reference](https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part2-stix-objects.html)
for different fields in each type of object.

*Example: Get all entities which have the substring "Rundll32" in their name
and has `type` equal to "attack-pattern"*

    $ http -j -vv POST http://localhost:5000/api/entities/filter/ name='Rundll32' type='attack-pattern'
    POST /api/entities/filter/ HTTP/1.1
    Accept: application/json, */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Content-Length: 46
    Content-Type: application/json
    Host: localhost:5000
    User-Agent: HTTPie/0.9.9

    {
        "name": "Rundll32",
        "type": "attack-pattern"
    }

    HTTP/1.0 200 OK
    Content-Length: 3621
    Content-Type: application/json
    Date: Mon, 15 Oct 2018 13:38:06 GMT
    Server: Werkzeug/0.14.1 Python/3.6.5

    [
        {
            [...]
            "modified": "2018-04-18T17:59:24.739Z",
            "name": "Rundll32",
            "type": "attack-pattern",
            [...]
        }
    ]

## Exploring the Yeti graph

### `/api/{entities,indicators}/{id}/neighbors/`

Given an object, get all objects that are connected to it. These connections are
represented by [STIX 2 Relationship](https://docs.oasis-open.org/cti/stix/v2.0/cs01/part2-stix-objects/stix-v2.0-cs01-part2-stix-objects.html#_Toc496714337) objects and have all expected [properties](https://docs.oasis-open.org/cti/stix/v2.0/cs01/part2-stix-objects/stix-v2.0-cs01-part2-stix-objects.html#_Toc496714340).

**Method and endpoint**

* `GET /api/{entities,indicators}/{id}/neighbors/`

**Response**

A JSON object with two keys:

  * `edges`: A list of serialized STIX 2 Relationship objects.
  * `vertices`: An `{id: object}` dictionary containing all neighboring objects.

You can reconstruct the graph based on the different object IDs in each item contained in the `edge` key.

*Example: Get all neighbors for the object `attack-pattern--322bad5a-1c49-4d23-ab79-76d641794afa`*

    $ http -vv GET http://localhost:5000/api/entities/attack-pattern--322bad5a-1c49-4d23-ab79-76d641794afa/neighbors/
    HTTP/1.0 200 OK
    Content-Length: 50952
    Content-Type: application/json
    Date: Mon, 15 Oct 2018 13:51:03 GMT
    Server: Werkzeug/0.14.1 Python/3.6.5

    {
    "edges": [...]
    "vertices": {
        "course-of-action--d8787791-d22e-45bb-a9a8-251d8d0a1ff2": {...},
        "intrusion-set--16ade1aa-0ea1-4bb7-88cc-9079df2ae756": {...},
        ...
    }
