# secam-tbc-2-yuv
GNU radio based graph to convert secam based TBC files of the vhs-decode project to a YUV file, which then can be further processed with ffmpeg.
The graph is based on Gnuradio 3.10

## Usage
Load the graph in GnuRadio Companion. As file sources select the \*.tbc and \*\_chroma.tbc files. At the very right of the graph define the output-file. It defaults to YUV.bin.
Run the graph. There is no real indication if the script is finished. So check if the output file still grows and the date when it last was written. If this doesn't change anymore for a while the writing is probably finished. Stop the graph.

In the next step use ffmpeg to convert that raw YUV file.
Example ffmpeg command:
*ffmpeg -f rawvideo -pix_fmt yuv444p -video_size 1135x624 -r 25 -i YUV.bin -c:v ffv1 -coder 1 -context 1 -g 25 -level 3 -slices 16 -slicecrc 1 -top 1 output.mkv*

The video dimensions of the file are 1135x624 with 25fps. Rendering out as ffv1 is recommended. As the width of the video is not divideable by 2, cropping has to be done in a video editor like virtualdub2 or using avisynth. Not doing so will make it not work in non linear editing programs. Also encoding to h.264 and other video formats will not work without cropping.
The output should be a proper interlaced video, thus can be properly deinterlaced if needed.

## Limitations
This is an experiemtal solution to decode SECAM video from the vhs / ld-decode project. There is a flaw on the right edge of the video. So part of the video will be overpainted in pink color. Depending on the input file also the whole video window can get overpainted by this. The cause and a solution is yet unkown.
The demodulation and filtering of color is very basic. There can be a lot of sparks in the color (secam fire), depending on how good or bad the SNR of the decoded input is.
No dropout compensation is present, as this is something usually done by the ld-decode components.

Any flaws present can be, to a certain degree, alleviated in post.
