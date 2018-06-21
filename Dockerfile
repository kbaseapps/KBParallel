FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer
# -----------------------------------------

# RUN apt-get update

# Here we install a python coverage tool and an
# https library that is out of date in the base image.

RUN pip install coverage

# update security libraries in the base image
RUN pip install cffi --upgrade \
    && pip install pyopenssl --upgrade \
    && pip install ndg-httpsclient --upgrade \
    && pip install pyasn1 --upgrade \
    && pip install requests --upgrade \
    && pip install 'requests[security]' --upgrade

# -----------------------------------------

WORKDIR /kb/module

RUN echo building njs wrapper anew && \
    cd /kb/dev_container/modules && \
    rm -rf njs_wrapper && \
    git clone https://github.com/kbase/njs_wrapper && \
    cd njs_wrapper && \
    git checkout develop && \
    . /kb/dev_container/user-env.sh && \
    rsync -avp /kb/dev_container/modules/njs_wrapper/lib/biokbase/njs_wrapper/ /kb/deployment/lib/biokbase/njs_wrapper/

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod 777 /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
