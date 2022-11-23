#FROM alpine as intermediate
#MAINTAINER leo.cazenille@gmail.com
#
## Install git and ssh
#RUN apk --no-cache --update-cache add git openssh-client
#
### Add credentials on build
##ARG SSH_PRIVATE_KEY
##RUN \
##    mkdir /root/.ssh/ && \
##    echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa && \
##    chmod 0600 /root/.ssh/id_rsa
#
## Make sure your domain is accepted
#RUN \
#    mkdir /root/.ssh/ && \
#    touch /root/.ssh/known_hosts && \
#    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
#
## Download repositories
##RUN git clone git@bitbucket.org:AubertKato/bioneat.git
##RUN git clone git@bitbucket.org:leo-cazenille/daccad-qd.git
#RUN git clone https://leo-cazenille@bitbucket.org/leo-cazenille/daccad-qd.git


########################
#FROM lcazenille/ubuntupython3andjava
FROM lcazenille/bioneatandpython:SSCI2019
#FROM lcazenille/bioneatandpython

# Update system and install openssh
RUN \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -yq openssh-server openssh-client rsync && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /home/user

# Create ssh key
RUN \
    mkdir /home/user/.ssh && \
    ssh-keygen -q -t rsa -N '' -f /home/user/.ssh/id_rsa && \
    cat /home/user/.ssh/id_rsa.pub > /home/user/.ssh/authorized_keys

# Copy repositories
#COPY --from=intermediate /bioneat /home/user/bioneat
#COPY --from=intermediate /daccad-qd /home/user/daccadqd
RUN git clone https://leo-cazenille@bitbucket.org/leo-cazenille/daccad-qd.git /home/user/daccadqd
RUN git clone -b reservoir https://mika1315@bitbucket.org/AubertKato/daccadevo.git /home/user/daccadevo
# Remove git directories (we can not use them because we would need private credentials)
RUN \
    mv /bioneat /home/user/bioneat && \
    rm -fr /home/user/daccadqd/.git*

RUN pip3 install -U git+https://gitlab.com/leo.cazenille/qdpy.git@develop

RUN pip3 install --upgrade --no-cache-dir -r /home/user/daccadevo/requirements.txt

# Prepare for entrypoint execution
#CMD ["bash"]
ENTRYPOINT ["/home/user/daccadqd/entrypoint.sh"]
#CMD ["1000", "normal"]

# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
