#################
### variables ###
#################

ARG PYTHON_VERSION=3.8-slim

#########################
### build environment ###
#########################

FROM python:${PYTHON_VERSION}

# Enter your GitHub token
ENV GH_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxx

# Enter your repository URL. For example - /your-login/your_repository.git
ENV REPO_URL=/your-login/your_repository.git


ENV HOME /home/ng_parser

ADD . $HOME

RUN apt-get update && apt-get install -y gnupg && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E1DD270288B4E6030699E45FA1715D88E1DF1F24 && \
    echo 'deb http://ppa.launchpad.net/git-core/ppa/ubuntu trusty main' > /etc/apt/sources.list.d/git.list && \
    apt-get install -y git && \
    python -m pip install --upgrade pip && \
    pip install -r $HOME/requirements.txt && \
    rm $HOME/requirements.txt

RUN /usr/sbin/useradd --create-home --home-dir /home/ng_parser --shell /bin/bash ng_parser

RUN chown -R ng_parser:ng_parser $HOME
USER ng_parser

WORKDIR $HOME
RUN ls | grep -v .py$| xargs rm -rf
ENTRYPOINT ["python", "ng_parser.py"]