SUDO_DOCKER ?= 
DOCKER_IMAGE_NAME ?= "ksd-build-test"

# build:
# 	echo "build"
# 	$(SUDO_DOCKER) docker build -t $(DOCKER_IMAGE_NAME) \
# 		python:3.10 -v .:/src/ -- bash
		
	  

shell: 
	$(SUDO_DOCKER) docker run --rm -it \
		-w /src/  -v `pwd`:/src/ python:3.11  bash
		
test: 
	$(SUDO_DOCKER) docker run --rm -it \
		-w /src/ -v `pwd`:/src/ python:3.11  sh -c "\
		pip install -e /src/[tests] && \
		pytest -vvv /src/tests/"
		
		