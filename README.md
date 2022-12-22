# secam-tbc-2-yuv
GNU radio based graph to convert secam based TBC files of the vhs-decode project to a YUV file, which then can be further processed with ffmpeg.
The graph is based on Gnuradio 3.10

## Graphs
Color values are set to properly decode color of TBC files who were decoded by using the MESECAM option in vhs-decode. Also MESECAM option should be the preferred one for decoding, as there are less color streaks in the decoded video.

## Usage
Load the graph in GnuRadio Companion. As file sources select the \*.tbc and \*\_chroma.tbc files. At the very right of the graph define the output-file. It defaults to YUV.bin.
Run the graph. There is a color video preview in the graph. It will slow down the conversion, but it's highly recommend to use it, as you can live check if the video flaps to pink at some point.

In the next step use ffmpeg to convert that raw YUV file.
```
ffmpeg -f rawvideo -pixel_format yuv444p -color_range tv -color_primaries "bt470bg" -color_trc "gamma28" -colorspace "bt470bg" -video_size 1185x624 -r 25 -i YUV.bin -filter:v "crop=928:576:183:46, setdar=1856/1383" -c:v ffv1 -coder 1 -context 1 -g 25 -level 3 -slices 16 -slicecrc 1 -top 1 output.mkv
```
It also crops the video to the same dimensions and cutout as it would be from the gen_chroma_vid script. This way it is possible to merge the chroma and luma planes from the normal ld-chroma-decoder and the gnuradio graph output in order to benefit from dropout correction.

The video dimensions of the file is 928x576, with 25fps. Rendering out as ffv1 is recommended.
The output should be a proper interlaced video, thus can be properly deinterlaced if needed.

## Merge color with dropout corrected MKV file
1. Create the YUV file with the GNURadio graph
2. Render this as MKV file as explained in this docu
3. create the video file as usual with the gen_chroma_vid script from vhs / ld-decode project
7. Merge the files and planes using the following command

```
ffmpeg -y -i "videofromgnuradio" -ss 0.00 -i "videofromgenvidscript  " -filter_complex " [0:v]format=yuv444p[0v]; [1:v]format=yuv422p10le[1v]; [0v][1v]mergeplanes=0x100102:yuv422p10le[v]" -map 1:a -c:a copy -map '[v]' -an -c:v ffv1 -coder 1 -context 1 -g 25 -level 3 -slices 16 -slicecrc 1 -top 1 "video_merged.mkv"
```
The order is important, as the mapping is as follows in the output.
Y of 2nd input -> Y, U of 1st input -> U, V of 1st input -> V

You can also omit one step and directly merge the YUV file from Gnuradio with the gen_chroma_vid generated file.
```
ffmpeg -y -f rawvideo -pixel_format yuv444p -color_range tv -color_primaries "bt470bg" -color_trc "gamma28" -colorspace "bt470bg" -video_size 1185x624 -r 25 -i "videofromgnuradio" -ss 0.00 -i "videofromgenvidscript" -filter_complex "[0:v]format=yuv444p, crop=928:576:183:46, setdar=1856/1383[chroma]; [1:v]format=yuv422p10le, setdar=1856/1383[luma]; [chroma][luma]mergeplanes=0x100102:yuv422p10le[v]" -map 1:a -c:a copy -map '[v]' -c:v ffv1 -coder 1 -context 1 -g 25 -level 3 -slices 16 -slicecrc 1 -top 1 "video_merged.mkv"
```
**In both cases the -ss option is important to align both files. Set it from 0.00 to 0.04 if your startfield is 2!**\
0.04 means 1/25th of a second, representing skipping one frame at the beginning from the gen_chroma_vid generated file.

## Limitations
This is an experimental solution to decode SECAM video from the vhs / ld-decode project. A flaw where the right border is pink has been fixed with a workaround. Depending on the input file also the whole video window can get overpainted by this. The cause and a solution is yet unkown.
The demodulation and filtering of color is very basic. There can be a lot of sparks in the color (secam fire), depending on how good or bad the SNR of the decoded input is.
No dropout compensation is present, as this is something usually done by the ld-decode components. But it can be added for the luma (Y) component, see the merge color section.

Flaws present can be, to a certain degree, alleviated in post.

## Troubleshooting
If the majority of the video is affected by pink overpainting there are two possible solutions to fix that.
### 1. Give the input files an offset
To shift the offset by one frame we have to take account, that one field in this graph is 1135 samples per line over 626 lines. So the formula is (1135*626)*startfield. \
The startfield is a variable that should be toggled between 0 and 2. Theoretically it can be anything between zero and the last field of the video. So use this to find a start frame where both fields are not pink. (As said usually only 0 and 2 make sense)
### 2. Decode by using --start parameter
Try to decode with --start <framenumber> option in vhs-decode. This will start the decode from another frame and reverts this effect. You might have to try out several start frames for success. But this is less convenient than option 1.
