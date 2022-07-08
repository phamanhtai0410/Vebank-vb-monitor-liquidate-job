
# **Vebank MONITOR LIQUIDATION**

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

## Release v1.0 



## 1. Run worker lending on staging
```
python3 tasks/consumer_lending.py -e lending-actions -k lending.supply -q queue-lending-supply
python3 tasks/consumer_lending.py -e lending-actions -k lending.borrow -q queue-lending-borrow
python3 tasks/consumer_lending.py -e lending-actions -k lending.repay -q queue-lending-repay
python3 tasks/consumer_lending.py -e lending-actions -k lending.withdraw -q queue-lending-withdraw
python3 tasks/consumer_lending.py -e lending-actions -k lending.reserve_update -q queue-lending-reserve_update
```
## 2. Run worker lending on local
```
python3 tasks/consumer_lending.py -e lending-actions -k lending.supply -q queue-local-lending-supply
python3 tasks/consumer_lending.py -e lending-actions -k lending.borrow -q queue-local-lending-borrow
python3 tasks/consumer_lending.py -e lending-actions -k lending.repay -q queue-local-lending-repay
python3 tasks/consumer_lending.py -e lending-actions -k lending.withdraw -q queue-local-lending-withdraw
python3 tasks/consumer_lending.py -e lending-actions -k lending.reserve_update -q queue-local-lending-reserve_update
```
## 3. Run worker pool on staging
```
python3 tasks/consumer_pool.py -e pool-actions -k pool.pair_created -q queue-pool-pair_created
```
