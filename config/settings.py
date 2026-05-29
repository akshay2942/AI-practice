"""Application settings and environment configuration."""

import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")

VALID_USER = os.getenv("TEST_USER", "standard_user")
VALID_PASSWORD = os.getenv("TEST_PASSWORD", "secret_sauce")
LOCKED_OUT_USER = os.getenv("LOCKED_USER", "locked_out_user")

DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "10000"))
