FROM tensorflow/tensorflow:0.9.0
MAINTAINER vsochat@stanford.edu

RUN apt-get update 
RUN apt-get -y install libtiff5-dev
RUN apt-get -y install libtiff5-dev
RUN apt-get -y install build-essential
RUN apt-get -y install cmake
RUN apt-get -y install libgtk2.0-dev
RUN apt-get -y install libjpeg8-dev
RUN apt-get -y install zlib1g-dev
RUN apt-get -y install libfreetype6-dev 
RUN apt-get -y install liblcms2-dev
RUN apt-get -y install libwebp-dev 
RUN apt-get -y install tcl8.6-dev
RUN apt-get -y install tk8.6-dev
RUN apt-get -y install wget
RUN apt-get -y install unzip
RUN apt-get -y install python-tk
RUN apt-get -y install python-dev 
RUN apt-get -y install pkg-config
RUN apt-get -y install libffi-dev 
RUN apt-get -y install libssl-dev
RUN apt-get -y install qt-sdk
RUN apt-get -y install libavcodec-dev 
RUN apt-get -y install libavformat-dev
RUN apt-get -y install libswscale-dev
RUN apt-get -y install libjpeg-dev
RUN apt-get -y install libpng-dev
RUN apt-get -y install libtiff-dev
RUN apt-get -y install libjasper-dev

# Software dependencies. 
# This is equivalent of requirements.txt, run on image build
RUN pip install --upgrade pip
RUN pip install cycler==0.10.0
RUN pip install h5py==2.6.0
RUN pip install matplotlib==1.5.3
RUN pip install nose==1.3.7
RUN pip install numpy==1.11.0
RUN pip install pandas==0.18.1
RUN pip install Pillow==3.2.0
RUN pip install pydicom==0.9.9
RUN pip install pyparsing==2.1.10
RUN pip install python-dateutil==2.5.3
RUN pip install pytz==2016.4
RUN pip install runcython==0.2.5
RUN pip install scipy==0.18.1
RUN pip install six==1.10.0
RUN pip install simplejson

# Build and install OpenCV
RUN wget https://github.com/Itseez/opencv/archive/3.1.0.zip
RUN unzip 3.1.0.zip
RUN rm 3.1.0.zip
RUN wget https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
RUN unzip 3.1.0.zip
RUN mkdir -p opencv-3.1.0/build
WORKDIR opencv-3.1.0/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.1.0/modules \
    -D PYTHON_EXECUTABLE=/usr/bin/python \
    -D BUILD_EXAMPLES=ON ..
RUN make -j4
RUN make install
RUN ldconfig

# Make directories for code and data
RUN mkdir /code
RUN mkdir /data

# Add the code
ADD . /code

# Download data models
RUN wget https://stanford.box.com/shared/static/t8hvcgy4m5kh5m76pt9kg9s71kjmik6c.meta -O /code/boneage/data/bone-age-checkpoint.ckpt-19999.meta
RUN wget https://stanford.box.com/shared/static/5936ydxx4qjk9rjkm1aun5fa9g5h27tt.ckpt-19999 -O /code/boneage/data/bone-age-checkpoint.ckpt-19999

# Clean up
RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN chmod u+x /code/boneage/cli.py

WORKDIR /code/boneage
ENTRYPOINT ["/usr/bin/python","/code/boneage/cli.py"]
