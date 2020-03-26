# dva project

## Prerequisites

- [Node.js v12.x](https://nodejs.org/en/) for client
- [Yarn](https://classic.yarnpkg.com/en/docs/install) for client
- [Python 3.7.6](https://www.python.org/downloads/release/python-376/) for server
- [Docker](https://www.docker.com/products/docker-desktop) and `docker-compose` installed if you're working on production builds.

## Local Development with Client

```
cd services/client
yarn install
yarn run
```

Go to [localhost:3000](localhost:3000) to see the client being served up

## Local Development with Server

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

### Running server:

Within virtualvenv run the following

```
python ./manage.py runserver
```

Go to [localhost:8000](localhost:8000) to see the django server. Eventually the server won't have a ui, and will just be our api server.

## Docker

### Usage

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

### Connecting to a container

```bash
docker exec -it ${CONTAINER_NAME} /bin/sh -c "[ -e /bin/bash ] && /bin/bash || /bin/sh"
```

### Connecting to db and running postgres commands

```bash
docker exec db psql -U postgres
```

## Git workflow

```
# create and checkout a branch
git checkout -b MyBranchName master

# stage and add new changes
git add .

# commit your changes
git commit -am "Commit message"

# if you've never published the branch run
git push -u origin MyBranchName

# otherwise run
git push
```
