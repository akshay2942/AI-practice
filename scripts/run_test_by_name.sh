#!/usr/bin/env bash
# Run pytest by test function name.
# Usage: ./scripts/run_test_by_name.sh test_catalog_lists_products
#        ./scripts/run_test_by_name.sh test_catalog_lists_products --headed

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <test_function_name> [--headed] [--browser-channel=chrome]"
  echo "Example: $0 test_catalog_lists_products --headed"
  exit 1
fi

TEST_NAME="$1"
shift

cd "$(dirname "$0")/.."
pytest -k "${TEST_NAME}" "$@"
