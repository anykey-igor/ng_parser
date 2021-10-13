#################
### variables ###
#################

ARG PYTHON_VERSION=3.8

#########################
### build environment ###
#########################

FROM python:${PYTHON_VERSION}

ENV GH_TOKEN=your GH token

ENV REPO_URL= Your repository for LOG file /username/reponame.git

RUN mkdir /ng_parser

WORKDIR /ng_parser
ADD requirements.txt /ng_parser/
RUN pip install -r requirements.txt
ADD access.log /ng_parser/
RUN rm requirements.txt
COPY ng_parser.py /ng_parser/
COPY .gitconfig /root

ENTRYPOINT ["python", "ng_parser.py"]