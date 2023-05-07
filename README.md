# Python - FFMPEG - Quality Reducer

I wrote this script mostly for fun to automate video squeezing and stretching several times. 

## REQUIREMENTS
* ffmpeg
* python3

## USAGE

```
usage: python reduce-quality.py [-h] [-i ITERATIONS] [-d DOWNSCALE_BY] [-c] filename

This script is a wrapper for ffmpeg. It squeeses and stretches out the video several times to reduce video quality.

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -i ITERATIONS, --iterations ITERATIONS
                        Number of downscale-upscale iterations. Default = 2.
  -d DOWNSCALE_BY, --downscale-by DOWNSCALE_BY
                        Downscale video by <int>. Default = 2.
  -c, --cleanup         Optional. Delete in-between iterations (to save space).
```