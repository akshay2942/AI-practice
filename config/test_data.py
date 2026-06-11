"""Test data loaders for parameterized scenarios."""

import json
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_SAUS01_ACCOUNTS_FILE = _DATA_DIR / "saus01_accounts.json"


def load_saus01_accounts() -> list[dict]:
    """Load Saus01 login accounts with username and password from JSON."""
    with _SAUS01_ACCOUNTS_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    password = data["password"]
    return [
        {
            "username": account["username"],
            "password": password,
            "expected_success": account["expected_success"],
        }
        for account in data["accounts"]
    ]


SAUS01_ACCOUNTS = load_saus01_accounts()
