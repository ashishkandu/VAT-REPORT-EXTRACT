FROM python:slim-buster
LABEL Ashish Kandu <ashishkandu43@gmail.com>

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG UID
ARG GID

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install ODBC Driver 17 for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install Python dependencies

# Copy requirements and install dependencies
COPY ./requirements.txt /tmp/requirements.txt


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

# Create the /backup directory
RUN mkdir /backup

RUN addgroup --gid $GID ashish && \
    adduser --uid $UID --gid $GID --disabled-password --gecos "" ashish

RUN chown -R ashish:ashish /backup
RUN chmod 755 /backup

USER ashish

# Copy project
COPY ./app .

ENV PATH="/py/bin:$PATH"

ENV TZ=Asia/Kathmandu