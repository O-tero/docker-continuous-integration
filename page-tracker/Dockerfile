FROM python:3.11.2-slim-bullseye AS builder

RUN apt-get update && \
    apt-get upgrade --yes

RUN useradd --create-home realpython
USER realpython
WORKDIR /home/realpython

ENV VIRTUALENV=/home/realpython/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=realpython pyproject.toml constraints.txt ./
RUN python -m pip install --upgrade pip setuptools && \
    python -m pip install --no-cache-dir -c constraints.txt ".[dev]"

COPY --chown=realpython src/ src/
COPY --chown=realpython test/ test/

RUN python -m pip install . -c constraints.txt

# Add separate RUN commands to isolate the failing step
RUN python -m pytest test/unit/
RUN python -m flake8 src/
RUN python -m isort src/ --check
RUN python -m black src/ --check --quiet
RUN python -m pylint src/ --disable=C0114,C0116,R1705
RUN python -m bandit -r src/ --quiet

# Build the wheel after all checks have passed
RUN python -m pip wheel --wheel-dir dist/ . -c constraints.txt

FROM python:3.11.2-slim-bullseye

RUN apt-get update && \
    apt-get upgrade --yes

RUN useradd --create-home realpython
USER realpython
WORKDIR /home/realpython

ENV VIRTUALENV=/home/realpython/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --from=builder /home/realpython/dist/page_tracker*.whl /home/realpython

RUN python -m pip install --upgrade pip setuptools && \
    python -m pip install --no-cache-dir page_tracker*.whl

CMD ["flask", "--app", "page_tracker.app", "run", \
    "--host", "0.0.0.0", "--port", "5000"]
