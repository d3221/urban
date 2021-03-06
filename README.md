# urban

## Pre-requests
* `sudo apt-get update && sudo apt-get upgrade`
* `sudo raspi-config` (Enable at Interfacing Options: Camera, SSH, SPI)
* `sudo nano /etc/modules` add lines at the end (enables camera on boot): 

```
# camera with v4l2 driver
bcm2835-v4l2
```



## Installation of OpenCV2 (3.0.0) on a RPi(3)
Type in the lines one after one (complete command line):

`sudo apt-get update && sudo apt-get upgrade`

`sudo apt-get install build-essential libgdk-pixbuf2.0-dev libpango1.0-dev libcairo2-dev git cmake pkg-config libjpeg8-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libgtk2.0-dev libatlas-base-dev gfortran -y`

`git clone https://github.com/Itseez/opencv.git && cd opencv && git checkout 3.0.0`

`sudo apt-get install python2.7-dev`

`cd ~ && wget https://bootstrap.pypa.io/get-pip.py && sudo python get-pip.py`

`pip install numpy`

`cd ~/opencv && mkdir build && cd build`

```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
 -D CMAKE_INSTALL_PREFIX=/usr/local \
 -D INSTALL_PYTHON_EXAMPLES=ON \
 -D INSTALL_C_EXAMPLES=ON \
 -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
 -D BUILD_EXAMPLES=ON ..
 ```
 
 `make -j4`
 
 `sudo make install && sudo ldconfig`
 
 
## Load this repo
`cd ~ && git clone https://github.com/d3221/urban`
