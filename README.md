
# **Vebank MONITOR LIQUIDATION JOBS**

## Environment
- docker
- docker-compose

## Notes
- Changes in docker-compose.yml: exposed port, image name, container name
- Changes in supervisord.conf: log files' location

## Use with docker, docker-compose
JUST RUN: `> docker-compose up -d --build`

## Health check
```curl -i <prefix>/common/health_check```

## Container env config:
```/webapps/.env```
<!-- 
## Run get logs

```python scripts/get_logs.py contract=<Name in DefaultConfig> event=<event name in smc> abi_path=<path> handle=<function handle in tasks - celery worker> from_block=<block number>```

## Run listen event

```python scripts/listener.py contract=<Name in DefaultConfig> event=<event name in smc> abi_path=<path> handle=<function handle in tasks - celery worker>``` 


## Release v1.0 

```
# listen event emit logs in time
python3 scripts/listener.py contract=CONTRACT_LENDING_POOL handle=marketplace_event_sale abi_path=abi/pool.json  event=Supply 

# Run worker 
celery --app tasks.task worker -Q vebank-smc-jobs -l DEBUG -c 4
```

## Running Command
```
python3 scripts/listener.py contract=CONTRACT_LENDING_POOL handle=lending_event_supply abi_path=lib/abi/Pool.json  event=Supply
```
  -->
