from .monitor_health_factor import rest_monitor_liquidation
from .root import rest_root

DEFAULT_BLUEPRINTS = [
    rest_root,
    rest_monitor_liquidation
]
