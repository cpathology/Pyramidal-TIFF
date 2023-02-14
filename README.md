# Pyramidal-Tiff
Conversion virtual slide format to pyramidal tiff

## 1. Docker image 
* Build from Dockerfile
```
$ docker build -t pyramidal_tiff:ping .
```

## 2. Docker container running
```
$ docker run -it --rm --user $(id -u):$(id -g) \
  -v /rsrch1/ip/pchen6/Codes/CHEN/Pyramidal-Tiff:/App/Pyramidal-Tiff \
  -v /rsrch1/ip/pchen6/MPRData:/Data \
  --shm-size=224G --cpuset-cpus=20-39 \
  --name pyramidal_tiff_ping pyramidal_tiff:ping
```