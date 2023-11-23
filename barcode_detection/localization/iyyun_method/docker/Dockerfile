FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev \
libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev \
libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev unzip

RUN apt-get install -y wget

RUN cd \
    && wget https://github.com/opencv/opencv/archive/3.2.0.zip \
    && unzip 3.2.0.zip \
    && cd opencv-3.2.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make -j8 \
    && make install \
    && cd \
    && rm 3.2.0.zip

RUN cd \
    && wget https://github.com/opencv/opencv_contrib/archive/3.2.0.zip \
    && unzip 3.2.0.zip \
    && cd opencv-3.2.0/build \
    && cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.2.0/modules/ .. \
    && make -j8 \
    && make install \
    && cd ../.. \
    && rm 3.2.0.zip

WORKDIR /workspace 
COPY main1.cpp main.cpp
COPY tests tests

RUN mkdir output
RUN git clone  https://github.com/iyyun/Barcode_1D.git \
    && rm /workspace/Barcode_1D/src/Linux/tencon/main.cpp \
    && mv /workspace/main.cpp /workspace/Barcode_1D/src/Linux/tencon \
    && cd Barcode_1D/src/Linux/tencon \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make

CMD ["./Barcode_1D/src/Linux/tencon/build/iyBarcode", "--file=/workspace/tmp_for_img/img.png"]
