VidY=FFmpegSource2("vhs-decode-generated-mkv.mkv", vtrack=-1,  cache=True, cachefile="", fpsnum=-1, fpsden=1, threads=-1, timecodes="", seekmode=1, overwrite=False, width=-1, height=-1, resizer="BICUBIC", colorspace="", rffmode=0, adjustdelay=-1, varprefix="")
VidY=VidY.ConvertTo8bit(bits=8)
# The trimming needs to be enabled when startfield is 2, otherwise disabled
VidY=VidY.trim(1,0)
# RawSourcePlus is an additional Plugin that has to be installed
VidUV=RawSourcePlus(file="Gnuradio-YUV.bin", width=1185, height=624, pixel_type="YUV444P8", fpsnum=25,fpsden=1)
# Video is cropped to perfectly overlay the other video
VidUV = VidUV.Crop(183, 46, -74, -2, align=False)
VidUV=VidUV.ConvertToYUV422(interlaced=true, matrix="601")
VidU=UToY(VidUV)
VidV=VToY(VidUV)
YToUV(VidU, VidV, VidY)
# Shifting Chroma in horizontal direction, use if chroma looks out of place
# The current Gnuradio Graph seems to have a deviation of 4 Pixels in the horizontal direction
Overlay(Last,X=4,Mode="Chroma")
