# first stage
FROM python:3.12 AS builder
WORKDIR /code
COPY requirements.txt ./

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --no-cache-dir -r requirements.txt --target /code/dependencies

# second unnamed stage
FROM python:3.12-slim

# Create a non-root user
RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --gid 1001 app && \
    mkdir -p /code/dependencies

WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder --chown=app:app /code/dependencies /code/dependencies
COPY --chown=app:app *.py .

USER app

ENV PYTHONPATH=/code/dependencies

ENTRYPOINT [ "python", "main.py" ] 
