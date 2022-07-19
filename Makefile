help: # Magic trick to gather command comments into a handy help message.
	@grep -E '^[a-zA-Z_-]+:.*?#- .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?#- "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv = venv
bin = ${venv}/bin/
python = ${bin}python
pip = ${bin}pip
pysources = lib/ tests/

install: #- Install dependencies
	python3 -m venv ${venv}
	${pip} install -U pip wheel setuptools
	${pip} install -r requirements.txt

test: #- Run the test suite
	${bin}pytest

format: #- Format code
	${bin}black ${pysources}
	${bin}isort ${pysources}

check: #- Check the code
	${bin}black --check ${pysources}
	${bin}flake8 ${pysources}
	${bin}mypy ${pysources}
	${bin}isort --check --diff ${pysources}

check-format: #- Format and check the code
	make format
	make check
	
check-organizations: #- Validate organizations schema
	${bin}python -m scripts.check_organizations organizations
