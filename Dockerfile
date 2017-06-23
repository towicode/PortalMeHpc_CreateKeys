FROM alpine:latest
MAINTAINER bcf_staff
RUN apk update
RUN apk add --update make cmake gcc g++ gfortran
RUN apk add --update python python-dev
RUN apk add --update openssh
RUN apk add --update py-pip

RUN pip install pycrypto
RUN pip install pexpect

ADD create_keys.py /usr/bin
RUN chmod +x /usr/bin/create_keys.py
ENTRYPOINT ["create_keys.py"]
