FROM lcazenille/bioneatandpython:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get update -yq && \
    apt-get install -yq rsync openjdk-17-jdk

# Make main folder
RUN mkdir -p /home/user

# Install python dependencies
RUN pip3 --no-cache-dir install tqdm git+https://gitlab.com/leo.cazenille/qdpy.git@develop


# Download repositories
RUN git clone https://bitbucket.org/AubertKato/daccad.git /home/user/daccad


# Install daccad
RUN cd /home/user/daccad; ./gradlew dist --no-build-cache

ENTRYPOINT ["/bin/bash","/home/user/daccadevo/entrypoint.sh"]