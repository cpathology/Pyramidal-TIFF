# Pyramidal-TIFF
Convert slides/images to pyramidal tiff

## 1. Docker environement
* Build docker image
```
$ docker build -t pyramidal_tiff:ping .
```

* Run docker container
```
$ docker run -it --rm --user $(id -u):$(id -g) \
  -v /rsrch1/ip/pchen6/Codes/CHEN/Pyramidal-Tiff:/App/Pyramidal-Tiff \
  -v /rsrch1/ip/pchen6/MPRData:/Data \
  --shm-size=224G --cpuset-cpus=20-39 \
  --name pyramidal_tiff_ping pyramidal_tiff:ping
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
