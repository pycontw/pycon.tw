## Getting Started
You can download the image with dockerhub or clone the source and build

## Create Container
`$ docker run -it --name {CONTAINER NAME} -p 8000:8000 freddy50806/pycontw:2019-dev /bin/bash`

## Run the server
In Container,pycontw website is preinstall in `/opt/pycon.tw/`
```
$ cd /opt/pycon.tw/src
$ python manage.py runserver 0.0.0.0:8000
```
and you can access the pycontw website with http://127.0.0.1:8000/ on your computer