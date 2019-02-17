# Docker

Prerequisites: You need [Docker](https://www.docker.com/community-edition) and
[docker-compose](https://docs.docker.com/compose/install/)

## Using `docker-compose`

We recommend using `docker-compose` to start your Yeti Docker container as it bundles
installations of most dependencies like ArangoDB and Redis.

These commands need to run in the `docker/` directory of the code, or use
`-f path/to/docker-compose.yaml` to poinpoint `docker-compose` to a given compose file.

### Run the applications

As simple as:

    $ docker-compose up

This command command will pre-populate the database with:

* content from MITRE so you can start playing with Yeti
* common STIX2 vocabularies
* common Kill Chains and TTPs including MITRE ATT&CK.
* a `admin@admin.com:RESETME` user that you can use to sign in

and start a working container listening for connections on `http://localhost:5000/`.

### Running `yetictl` in your container

You can still run `yetictl` from your container as you would from a regular server, e.g.:

    $ docker-compose exec yeti python3 ctl/yetictl.py reset-password admin@admin.com

Or also:

    $ docker exec <CONTAINER_ID> python3 ctl/yetictl.py reset-password admin@admin.com

## Local Docker image build

### Clone the repo

    $ git clone https://github.com/yeti-platform/TibetanBrownBear.git
    $ cd TibetanBrownBear

### Build the image

    $ docker build -t yetiplatform/tibetanbrownbear .

The tag `yetiplatform/tibetanbrownbear` will be used in the compose file.
