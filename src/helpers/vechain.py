from thor_requests.connect import Connect
from thor_requests.contract import Contract
from src.config import DefaultConfig
from pydash import get


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def get_health_factor(_user):
    # Establish connect to contracts
    connector = Connect(DefaultConfig.VECHAIN_RPC)

    # Contract iDelegateSeer
    _contract_address = DefaultConfig.CONTRACT_LENDING_POOL
    _contract_instance = Contract.fromFile('src/abis/PoolABI.json')

    # Call update
    _res = connector.call(
        DefaultConfig.CALLER,
        _contract_instance,
        "getUserAccountData",
        [_user],
        _contract_address
    )
    if not _res or get(_res, 'decoded')['healthFactor'] == 2**256 - 1:
        return 0

    return truncate(get(_res, 'decoded')['healthFactor'] / (10 ** 18), 3)
