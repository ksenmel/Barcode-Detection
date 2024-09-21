import os
from pathlib import Path

from barcode_detection.deblurring.deblur import Deblurrer


class DeblurRealEsrgan(Deblurrer):
    def deblur(self, path_to_video: str):
        video_path = Path(path_to_video)
        video_name = video_path.name

        owd = os.getcwd()  # initial working dir
        working_dir = "barcode_detection/deblurring/real_esrgan"

        tmp_frames_path = Path("barcode_detection/deblurring/real_esrgan/tmp_frames")
        out_frames_path = Path("barcode_detection/deblurring/real_esrgan/out_frames")

        # fix empty directory issue
        # maybe add try..except
        if tmp_frames_path.is_dir():
            tmp_frames_path.rmdir()
        else:
            tmp_frames_path.mkdir()

        if out_frames_path.is_dir():
            out_frames_path.rmdir()
        else:
            out_frames_path.mkdir()

        video_path.rename(working_dir + "/" + video_name)

        os.chdir(working_dir)

        # somehow add steps
        os.system(
            f"ffmpeg -i {video_name} -qscale:v 1 -qmin 1 -qmax 1 -vsync 0 tmp_frames/frame%08d.jpg"
        )
        os.system(
            "./realesrgan-ncnn-vulkan -i tmp_frames -o out_frames -n realesr-animevideov3 -s 2 -f jpg"
        )

        os.chdir(owd)  # back to initial working dir

        # need to place video back to dir we took it from or rewrite code here
