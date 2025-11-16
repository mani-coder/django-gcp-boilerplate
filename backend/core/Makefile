.PHONY: quality style

check_dirs := . --exclude .venv

# This target runs checks on all files
quality:
	black --check $(check_dirs)
	ruff $(check_dirs)
	isort --check-only --diff . --skip .venv

# This target runs checks on all files and potentially modifies some of them
style:
	black $(check_dirs)
	ruff --fix $(check_dirs)
	isort . --skip .venv
