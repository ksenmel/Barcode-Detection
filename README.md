# Barcode-Detection

## Features

### Localization
- [1D Barcode Localization](https://github.com/iyyun/Barcode_1D) by iyyun
- [onnx-yolov7](https://github.com/kirill-ivanov-a/onnx-yolov7)

### Decoding
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar/tree/master)
- [zxing](https://github.com/zxing/zxing)

## Build Instructions
To use 'iyyun', 'zxing' and 'pyzbar' methods, you need to first run Docker and build Docker images as in the instructions below
```
$ git clone https://github.com/ksenmel/Barcode-Detection
```
If you're a MacOS user, run this command as well:
```
$ open -a Docker
```
#### how to build iyyun with docker
```
$ cd Barcode-Detection/barcode_detection/localization/iyyun_method/docker
$ docker build -t iyyun_docker .
```
#### how to build zxing with docker
```
$ cd Barcode-Detection/barcode_detection/decoding/zxing_method/docker
$ docker build -t zxing_docker .
```
#### how to build pyzbar with docker
```
$ cd Barcode-Detection/barcode_detection/decoding/pyzbar_method/docker
$ docker build -t pyzbar_docker .
```


## Demo
```
$ cd Barcode-Detection
$ python3 main.py example/image.jpg pyzbar iyyun
$ python3 main.py example/image.jpg zxing yolov7 --detector_path /path/to/weights
```

You can download weights for 'yolov7' [here](https://drive.google.com/file/d/1yD_N2mRRvbNobSP-VDsfDY_mW2MmTS3l/view?usp=sharing)