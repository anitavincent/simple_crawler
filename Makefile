run:
	python3 __main__.py > ./data/log

test:
	python3 -m pytest

verbose:
	python3 __main__.py	

docker:
	docker-compose up > ./data/log

docker_verbose:
	docker-compose up