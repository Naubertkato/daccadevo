FROM python:3.14-slim

RUN DEBIAN_FRONTEND=noninteractive apt-get update -yq && \
    apt-get install -yq openjdk-21-jdk git

RUN pip install uv

# Make main folder
RUN mkdir -p /home/user

# Download repositories
RUN git clone https://bitbucket.org/AubertKato/daccad.git /home/user/daccad

# Install DACCAD
RUN cd /home/user/daccad; ./gradlew dist --no-build-cache

# Install python dependencies
RUN uv pip install --system --no-cache-dir tqdm torch git+https://AubertKato@bitbucket.org/AubertKato/daccadevo.git git+https://gitlab.com/leo.cazenille/qdpy.git@develop


ENTRYPOINT ["/bin/bash","/home/user/daccadevo/entrypoint.sh"]