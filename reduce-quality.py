import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(
    prog="Python - FFMPEG - Quality Reducer",
    description="""
    This script is a wrapper for ffmpeg. 
    It squeeses and stretches out the video several times to reduce video quality.
    """,
)

parser.add_argument("filename")
parser.add_argument(
    "-i",
    "--iterations",
    type=int,
    default=2,
    help="Number of downscale-upscale iterations. Default = 2.",
)
parser.add_argument(
    "-d",
    "--downscale-by",
    type=int,
    default=2,
    help="Downscale video by <int>. Default = 2.",
)
parser.add_argument(
    "-c",
    "--cleanup",
    action="store_true",
    help="Optional. Delete in-between iterations (to save space).",
)

args = parser.parse_args()

file = args.filename
iterations = args.iterations * 2
downscale_by = args.downscale_by
cleanup = args.cleanup

FILE_PREFIX = file.split(".")[0]
FILE_EXTENSION = file.split(".")[1]


# get original file's resolution
def get_resolution(filename):
    check_res_cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {filename}"
    resolution = bytes.decode(
        subprocess.check_output(check_res_cmd, shell=True)
    ).strip()

    global width, height
    width = int(resolution.split("x")[0])
    height = int(resolution.split("x")[1])

    print(f"Detected resolution: {width}x{height}")
    # return height, width


def transform_video(iterations):
    i = 1
    while i <= iterations:
        if i == 1:
            transform_res_cmd = f"ffmpeg -i {FILE_PREFIX}.{FILE_EXTENSION} -vf scale={width_downscaled}:{height_downscaled} {FILE_PREFIX}_{i}.{FILE_EXTENSION}"
            subprocess.check_output(transform_res_cmd, shell=True)
            # print(transform_res_cmd)
            i += 1
        if i == iterations:
            transform_res_cmd = f"ffmpeg -i {FILE_PREFIX}_{i-1}.{FILE_EXTENSION} -vf scale={width}:{height} {FILE_PREFIX}_final.{FILE_EXTENSION}"
            subprocess.check_output(transform_res_cmd, shell=True)
            # print(transform_res_cmd)
            if cleanup:
                rm_cmd = f"rm -f {FILE_PREFIX}_{i-1}.{FILE_EXTENSION}"
                subprocess.run(rm_cmd, shell=True)
            i += 1
        elif i < iterations and i % 2 == 0:
            transform_res_cmd = f"ffmpeg -i {FILE_PREFIX}_{i-1}.{FILE_EXTENSION} -vf scale={width}:{height} {FILE_PREFIX}_{i}.{FILE_EXTENSION}"
            subprocess.check_output(transform_res_cmd, shell=True)
            # print(transform_res_cmd)
            if cleanup:
                rm_cmd = f"rm -f {FILE_PREFIX}_{i-1}.{FILE_EXTENSION}"
                subprocess.run(rm_cmd, shell=True)
            i += 1
        elif i < iterations and i % 2 != 0:
            transform_res_cmd = f"ffmpeg -i {FILE_PREFIX}_{i-1}.{FILE_EXTENSION} -vf scale={width_downscaled}:{height_downscaled} {FILE_PREFIX}_{i}.{FILE_EXTENSION}"
            subprocess.check_output(transform_res_cmd, shell=True)
            # print(transform_res_cmd)
            if cleanup:
                rm_cmd = f"rm -f {FILE_PREFIX}_{i-1}.{FILE_EXTENSION}"
                subprocess.run(rm_cmd, shell=True)
            i += 1


try:
    get_resolution(file)
    width_downscaled = round(width / 4) if (width % 2) == 0 else round(width / 4) + 1
    height_downscaled = (
        round(height / 4) if (height % 2) == 0 else round(height / 4) + 1
    )
    transform_video(iterations)
except subprocess.CalledProcessError:
    print(f"[!] File {file} not found.")
    sys.exit(1)
