# secam-tbc-2-yuv
GNU radio based graph to convert secam based TBC files of the vhs-decode project to a YUV file, which then can be further processed with ffmpeg.
The graph is based on Gnuradio 3.10

## Graphs
secam_to_yuv.grc \
secam_to_yuv2.grc

The first one was the initial one. The second one has a workaround included so that the wrongly overpainted area is shifted out of the visible area of the video. Also color was corrected a bit to properly decode color of TBC files who were decoded by using the MESECAM option in vhs-decode. Also MESECAM option should be prefered for decoding, as there are less color streaks in the decoded video.

## Usage
Load the graph in GnuRadio Companion. As file sources select the \*.tbc and \*\_chroma.tbc files. At the very right of the graph define the output-file. It defaults to YUV.bin.
Run the graph. There is no real indication if the script is finished. However, there is a video preview in the graph, that can be activated. But it will slow down the conversion. So check if the output file still grows and the date when it last was written. If this doesn't change anymore for a while the writing is probably finished. Stop the graph.

In the next step use ffmpeg to convert that raw YUV file.

Example ffmpeg command:
```
ffmpeg -f rawvideo -pix_fmt yuv444p -video_size 1135x624 -r 25 -i YUV.bin -c:v ffv1 -coder 1 -context 1 -g 25 -level 3 -slices 16 -slicecrc 1 -top 1 output.mkv
```

If you use the second script, which should be the preferred one, the ffmpeg command is.
```
ffmpeg -f rawvideo -pixel_format yuv444p -color_range tv -color_primaries "bt470bg" -color_trc "gamma28" -colorspace "bt470bg" -video_size 1185x624 -r 25 -i YUV.bin -filter:v "crop=928:576:183:46" -c:v ffv1 -coder 1 -context 1 -g 25 -level 3 -slices 16 -slicecrc 1 -top 1 output.mkv
```
It also crops the video to the same dimensions and cutout as it would be from the gen_chroma_vid script. This way it is possible to merge the chroma and luma planes from the normal ld-chroma-decoder and the gnuradio graph output in order to benefit from dropout correction.

The video dimensions of the file are 1135x624, or 928x576 depending on the graph used, with 25fps. Rendering out as ffv1 is recommended. If the width of the video is not divideable by 2, cropping has to be done in a video editor like virtualdub2 or using avisynth. Not doing so will make it not work in non linear editing programs. Also encoding to h.264 and other video formats will not work without cropping.
The output should be a proper interlaced video, thus can be properly deinterlaced if needed.

## Merge color with dropout corrected MKV file
1. create the video file as usual with the gen_chroma_vid script from vhs / ld-decode project
2. Open it in an editor like virtualdub2, set compression to FFMPEG FFV1 lossless codec. In the config of the codec select 8 bit and YUV 4:4:4
3. Render out as new MKV file
4. Create the YUV file with the GNURadio graph
5. Render this as MKV file as explained in this docu
6. Merge the files and planes using the following command

```
ffmpeg -y -i "videofromgnuradio" -i "videofromgenvidscript  " -filter_complex " [0:v]format=yuv444p[0v]; [1:v]format=yuv444p[1v]; [0v][1v]mergeplanes=0x100102:yuv444p[v]" -map '[v]' -an -c:v ffv1 -coder 1 -context 1 -g 25 -level 3 -slices 16 -slicecrc 1 -top 1 "video_merged.mkv"
```
The order is important, as the mapping is as follows in the output.
Y of 2nd input -> Y, U of 1st input -> U, V of 1st input -> V

## Limitations
This is an experimental solution to decode SECAM video from the vhs / ld-decode project. There is a flaw on the right edge of the video. So part of the video will be overpainted in pink color. Depending on the input file also the whole video window can get overpainted by this. The cause and a solution is yet unkown.
The demodulation and filtering of color is very basic. There can be a lot of sparks in the color (secam fire), depending on how good or bad the SNR of the decoded input is.
No dropout compensation is present, as this is something usually done by the ld-decode components.

Flaws present can be, to a certain degree, alleviated in post.

## Troubleshooting
If the majority of the video is affected by pink overpainting there are two possible solutions to fix that.
### 1. Give the input files an offset
To shift the offset by one frame we have to take account, that one frame is 1135 samples per line over 626 lines. So the formula is (1135*626)*n. \
The n is a variable that can be anything between zero and the last frame of the video. It can be seen as a start-frame option. So use this to find a start frame where both fields are not pink.
### 2. Decode by using --start parameter
Try to decode with --start <framenumber> option in vhs-decode. This will start the decode from another frame and reverts this effect. You might have to try out several start frames for success. But this is less convenient than option 1.
