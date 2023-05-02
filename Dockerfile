FROM lcazenille/ubuntupython3andjava

# First, update Cython

RUN pip3 --no-cache-dir install -U Cython

# Install python dependencies
RUN pip3 --no-cache-dir install -U numpy pandas tqdm git+https://gitlab.com/leo.cazenille/qdpy.git@develop

# Make main folder
RUN mkdir -p /home/user

# Download repositories
RUN git clone https://bitbucket.org/AubertKato/daccad.git /home/user/daccad


# Install daccad
RUN cd /home/user/daccad; ./gradlew dist --no-build-cache

ENTRYPOINT ["/home/user/daccadevo/entrypoint.sh"]