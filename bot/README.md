# YTEssence
This telegram bot uses UI to download, preprocess and analyse videos by YouTube link.
___


### Run service in Python

Install all dependencies (libraries):
```bash
cd bot
pip3 install -r requirements.txt
```
Run bot:
```bash
python3 bot/main.py
```


### Run service in Docker container
Run: builds, (re)creates, starts, and attaches to containers for a service.
```bash
sudo docker-compose up -d --build
```
Stop running containers without removing them
```bash
sudo docker-compose stop
```
Display a live stream of container(s) resource usage statistics
```bash
sudo docker stats
```
Stops containers and removes containers, networks, volumes, and images created by `up`
```bash
sudo docker-compose down -v
```

More info about installing [Docker](https://docs.docker.com/get-docker/) and [Docker-Compose](https://docs.docker.com/compose/install/).
