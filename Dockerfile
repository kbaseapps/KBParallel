FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

# -----------------------------------------
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
