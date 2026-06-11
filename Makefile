.PHONY: test-core list-core test-core-headed test-case list-test-case test-case-headed

PYTEST := .venv/bin/pytest

# Run all tests marked @pytest.mark.core
test-core:
	$(PYTEST) -m core

# List core tests without executing them
list-core:
	$(PYTEST) -m core --collect-only -q

# Run core tests in headed Google Chrome
test-core-headed:
	$(PYTEST) -m core --headed --browser-channel=chrome

# Run a single test by function name (required: NAME=...)
# Example: make test-case NAME=test_catalog_lists_products
test-case:
	@test -n "$(NAME)" || (echo "Usage: make test-case NAME=<test_function_name>" && exit 1)
	$(PYTEST) -k "$(NAME)"

# List tests matching NAME without running
# Example: make list-test-case NAME=test_catalog_lists_products
list-test-case:
	@test -n "$(NAME)" || (echo "Usage: make list-test-case NAME=<test_function_name>" && exit 1)
	$(PYTEST) -k "$(NAME)" --collect-only -q

# Run test by name in headed Google Chrome
# Example: make test-case-headed NAME=test_standard_user_can_login
test-case-headed:
	@test -n "$(NAME)" || (echo "Usage: make test-case-headed NAME=<test_function_name>" && exit 1)
	$(PYTEST) -k "$(NAME)" --headed --browser-channel=chrome
