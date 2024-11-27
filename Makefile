.PHONY: setup
setup:
	uv sync
	uv run pre-commit install

.PHONY: test
test:
	uv run \
	pytest \
	--cov=src \
	--cov-report=term-missing
