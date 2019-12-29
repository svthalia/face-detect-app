FROM python:3.7

ARG install_dev_requirements=1
ARG source_commit="unknown"

EXPOSE 8000

RUN apt-get -y update
RUN apt-get install -y --fix-missing --no-install-recommends \
    postgresql-client \
    gettext \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libjpeg-dev \
    libpng-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.19' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

RUN mkdir -p /usr/log/ && \
    mkdir -p /usr/src/ && \
    touch /usr/log/uwsgi.log && \
    chown -R www-data:www-data /usr/log

COPY . /usr/src/
WORKDIR /usr/src/

# install python requirements
RUN if [ "$install_dev_requirements" -eq 1 ]; then \
        poetry install --no-interaction; \
    else \
        echo "This will fail if the dependencies are out of date"; \
        poetry install --no-interaction --no-dev; \
    fi; \
    poetry cache clear --all --no-interaction pypi

RUN apt-get clean && rm -rf /tmp/* /var/tmp/* && apt-get remove -y \
    build-essential \
    cmake \
    gfortran

# Create entry points
COPY resources/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY resources/entrypoint_production.sh /usr/local/bin/entrypoint_production.sh
RUN chmod +x /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint_production.sh

# Create log dir and log file
RUN mkdir /app && \
    mkdir -p /app/log/ && \
    touch /app/log/uwsgi.log && \
    chown -R www-data:www-data /app
