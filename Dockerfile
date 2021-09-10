### base image
FROM python:3.9-slim-buster AS base

RUN useradd --uid 1100 appuser --no-create-home
RUN apt-get update

RUN python -m venv /venv
ENV PATH="/venv/bin:${PATH}"

RUN mkdir /app
WORKDIR /app

### pin image
### This will re-pin the requirements for both the actual module as well
### as the additional test requirements
FROM base as pin
COPY --chown=appuser:appuser requirements/requirements.in /app/
COPY --chown=appuser:appuser requirements/test-requirements.in /app/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.in
RUN pip list --format freeze > /app/requirements.txt

RUN python -m venv /venv-test
ENV PATH="/venv-test/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/test-requirements.in
RUN pip list --format freeze > /app/test-requirements.txt


### requirements image
### this is the base image with installed requirements
FROM base as requirements
COPY --chown=appuser:appuser requirements/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


### test image
### This is the test image with additional installed test requirements
FROM requirements as test
COPY --chown=appuser:appuser requirements/test-requirements.txt /app/test-requirements.txt
RUN pip install --no-cache-dir -r /app/test-requirements.txt
COPY --chown=appuser:appuser . /app/
RUN python -m pip install --no-cache-dir -e /app
COPY --chown=appuser:appuser pytest.ini /tmp
USER 1100


