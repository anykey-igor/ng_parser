#################
### variables ###
#################

ARG PYTHON_VERSION=3.8

#########################
### build environment ###
#########################

FROM python:${PYTHON_VERSION}

RUN mkdir /ng_parser
WORKDIR /ng_parser
ADD requirements.txt /ng_parser/
RUN pip install -r requirements.txt
ADD . /ng_parser/
COPY ng_parser.py /ng_parser/

ENTRYPOINT ["python", "ng_parser.py"]