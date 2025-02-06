.PHONY: setup
setup:
	uv sync
	uv run pre-commit install

.PHONY: test
test:
	uv run \
	pytest \
	-s \
	--cov=src \
	--cov-report=term-missing

.PHONY: test-ci
test-ci:
	uv run \
	pytest \
	--cov=src \
	--cov-report=term-missing \
	--cov-report xml:coverage.xml \
	--junit-xml=report.xml

.PHONY: build
build:
	uv build

.PHONY: publish
publish:
	uv publish
