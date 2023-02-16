# Pyramidal-TIFF
Convert slides/images to pyramidal tiff

## 1. Docker environement
### a. Build docker image from Dockerfile
```
$ docker build -t pyramidal_tiff:chen .
```
* or pull from Docker Hub
```
$ docker pull pingjunchen/pyramidal_tiff:chen
$ docker tag pingjunchen/pyramidal_tiff:chen pyramidal_tiff:chen
```
### b. Run docker container
``` Start docker container (specify CODE_ROOT & DATA_ROOT)
$ docker run -it --rm --user $(id -u):$(id -g) \
  -v ${CODE_ROOT}:/App/Pyramidal-TIFF \
  -v ${DATA_ROOT}:/Data \
  --shm-size=128G --cpuset-cpus=0-19 \
  --name pyramidal_tiff_chen pyramidal_tiff:chen
```
* For example:
```
$ docker run -it --rm --user $(id -u):$(id -g) \
  -v /rsrch1/ip/pchen6/Codes/CHEN/Pyramidal-TIFF:/App/Pyramidal-TIFF \
  -v /rsrch1/ip/pchen6/Archive/TestData:/Data \
  --shm-size=128G --cpuset-cpus=0-19 \
  --name pyramidal_tiff_chen pyramidal_tiff:chen
```

## 2. Pyramidal tiff conversion
* Convert slides
```
$ python convert_slide.py
```

* Convert images
```
$ python convert_image.py
```
