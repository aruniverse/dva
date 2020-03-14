# dva

## Prerequisites

- You will need both [`docker`](https://www.docker.com/products/docker-desktop) and `docker-compose` installed.

## Usage

```bash
# Build the images
docker-compose build --parallel

# Fire the containers up & run it in the background
docker-compose up -d

# update containers later on
docker-compose up -d --build

# You can also start them in the background:
docker-compose start
```

## Connecting to a container

```bash
docker exec -it ${CONTAINER_NAME} /bin/sh -c "[ -e /bin/bash ] && /bin/bash || /bin/sh"
```

## Connecting to db and running postgres commands

```bash
docker exec db psql -U postgres
```

## Developing with server

I'd recommend using virtualenv to help manage & distinguish which packages are being used for this project. To get setup follow the below instructions.

```
cd services/server
pip install virtualenv
virtualenv venv
```

You'll have to now activate the virtual environment

### On Unix:

```
source venv/bin/activate
```

### On Windows:

```
venv/Scripts/activate.bat
```

To deactivate just run `deactivate`

If you add or update any packages being used, you should run `pip freeze > requirements.txt` while the virtualenv is activated.
