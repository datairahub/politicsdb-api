FROM python:3.10.6

WORKDIR /pdb

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev \
        build-essential \
        libgdal-dev \
        nano

RUN python -m pip install --upgrade pip

RUN pip3 install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"

RUN rm -rf /var/lib/apt/lists/* && \
    useradd -ms /bin/bash pdb && \
    chown -R pdb:pdb ./

USER pdb

COPY --chown=pdb:pdb . ./

RUN PATH=$PATH:/home/pdb/.local/bin

RUN pip install --no-cache-dir --user -r requirements.txt

RUN rm requirements.txt

WORKDIR /pdb/backend
