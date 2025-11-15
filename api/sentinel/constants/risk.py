"""Risk tolerance constants for validation."""

RISK_LEVELS = {
    'low': {'id': 0, 'label': 'Low'},
    'medium': {'id': 1, 'label': 'Medium'},
    'high': {'id': 2, 'label': 'High'},
}

VALID_RISK_KEYS = set(RISK_LEVELS.keys())
VALID_RISK_IDS = {0, 1, 2}
