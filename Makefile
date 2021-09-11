.PHONY: pin build-test test

pin:
	docker build --no-cache --target pin -t pythonarch:pin .
	docker cp $$(docker create pythonarch:pin):/app/requirements.txt requirements/requirements.txt
	docker cp $$(docker create pythonarch:pin):/app/test-requirements.txt requirements/test-requirements.txt

build-test:
	docker build --target test -t pythonarch:test .

test: build-test
	docker run --workdir=/tmp -v $$(pwd):/out --tty --rm pythonarch:test pytest /app/tests $(_pytest_internal) $(pytest)
