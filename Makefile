SUDO_DOCKER ?= 
DOCKER_IMAGE_NAME ?= "ksd-build-test"

build:
	$(SUDO_DOCKER) docker run --rm -it \
	    -u $(id -u ${USER}):$(id -g ${USER}) \
		-w /src/ -v `pwd`:/src/ python:3.11  sh -c "\
		pip install build twine && \
		python -m build && \
		twine check ./dist/*"

shell: 
	$(SUDO_DOCKER) docker run --rm -it \
		-w /src/  -v `pwd`:/src/ python:3.11  bash
		
test: 
	$(SUDO_DOCKER) docker run --rm -it \
		-u $(id -u ${USER}):$(id -g ${USER}) \
		-w /src/ -v `pwd`:/src/ python:3.11  sh -c "\
		pip install -e /src/[tests] && \
		pytest -vvv /src/tests/"
		
clean:
	$(SUDO_DOCKER) docker run --rm -it \
		-u $(id -u ${USER}):$(id -g ${USER}) \
		-w /src/ -v `pwd`:/src/ python:3.11  sh -c "\
	find . -name '*.pyc' -delete && \
	find . -type d -name __pycache__ -delete && \
	rm -rf ./dist/ && \
	rm -rf .pytest_cache && \
	rm -rf ./ksd.egg-info"
