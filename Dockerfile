FROM tensorflow/tensorflow:0.9.0
MAINTAINER vsochat@stanford.edu

RUN apt-get update && apt-get install -y libtiff5-dev \
                      libjpeg8-dev \
                      zlib1g-dev \
                      libfreetype6-dev \ 
                      liblcms2-dev \
                      libwebp-dev tcl8.6-dev \
                      tk8.6-dev \
                      python-tk

# Make directories for code and data
RUN mkdir /code
RUN mkdir /data

# Add the code
ADD . /code

# Install software dependencies
RUN pip install -r /code/boneage/requirements.txt

# Clean up
RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN chmod u+x /code/boneage/cli.py

ENTRYPOINT ["python","/code/boneage/cli.py"]
