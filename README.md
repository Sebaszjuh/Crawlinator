# CrawlinaTOR

## Prerequisites

- Docker
- Miniconda with python 3.7

## Setup

```conda create -n crawlinator```
```conda activate crawlinator```
```conda install --file requirements.txt```
```pip install elastic-app-search```

## Development

- Run ```docker-compose up```
- Go to [localhost:3002](http://localhost:3002)
- Create an engine called: `crawlinator`
- Go to [http://localhost:3002/as#/credentials](http://localhost:3002/as#/credentials)
- Copy the private key and replace it in `crawlinator/pipelines.py`
- Copy the search key and replace tin in `crawlinator-ui/src/config/engine.json`

You only have to do the above steps once everytime you run `docker-compose up`

To work on the Spider you do the following

1. Make changes to the spider
2. Run ```python go-spider.py```
3. Check if the results [here](http://localhost:3002/as#/engines/crawlinator/documents) or if there are errors check the `logs` directory
4. Repeat from step 1.
