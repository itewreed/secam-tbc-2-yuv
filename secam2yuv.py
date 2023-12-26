#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: secam TBC files to YUV file
# Author: itewreed, tony9954
# Description: Takes luma and secam chroma TBC files and generates YUV file
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import video_sdl
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class secam2yuv(gr.top_block, Qt.QWidget):

    def __init__(self, inputdir='/home/user/input/', outputdir='/home/user/output/', startfield=0, videofile='tbcfilename'):
        gr.top_block.__init__(self, "secam TBC files to YUV file", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("secam TBC files to YUV file")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "secam2yuv")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.inputdir = inputdir
        self.outputdir = outputdir
        self.startfield = startfield
        self.videofile = videofile

        ##################################################
        # Variables
        ##################################################
        self.sample_shift = sample_shift = 50
        self.line_length2 = line_length2 = 1135
        self.startfield_old = startfield_old = 2
        self.samp_rate = samp_rate = 1135/(64e-6)
        self.lines_per_frame_discard = lines_per_frame_discard = 1
        self.lines_per_frame = lines_per_frame = 625
        self.line_length = line_length = line_length2+sample_shift
        self.fm_demph = fm_demph = 150e-8
        self.colordelay = colordelay = 1070+sample_shift
        self.chroma_range_red = chroma_range_red = 12.90
        self.chroma_range_blue = chroma_range_blue = 12.45

        ##################################################
        # Blocks
        ##################################################

        self._chroma_range_red_range = Range(10, 14, 0.05, 12.90, 200)
        self._chroma_range_red_win = RangeWidget(self._chroma_range_red_range, self.set_chroma_range_red, "Color Red", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._chroma_range_red_win)
        self._chroma_range_blue_range = Range(10, 14, 0.05, 12.45, 200)
        self._chroma_range_blue_win = RangeWidget(self._chroma_range_blue_range, self.set_chroma_range_blue, "Color Blue", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._chroma_range_blue_win)
        self.video_sdl_sink_0_0_0_0 = video_sdl.sink_uc(0, (line_length+1), lines_per_frame, (line_length+1), lines_per_frame)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            10000, #size
            samp_rate, #samp_rate
            "", #name
            3, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-3, 255)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['green', 'blue', 'red', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_number_sink_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_1.set_update_time(0.10)
        self.qtgui_number_sink_1.set_title("Red Channel")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_1.set_min(i, -1)
            self.qtgui_number_sink_1.set_max(i, 1)
            self.qtgui_number_sink_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1.set_label(i, labels[i])
            self.qtgui_number_sink_1.set_unit(i, units[i])
            self.qtgui_number_sink_1.set_factor(i, factor[i])

        self.qtgui_number_sink_1.enable_autoscale(False)
        self._qtgui_number_sink_1_win = sip.wrapinstance(self.qtgui_number_sink_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_1_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("Blue Channel")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.hilbert_fc_0 = filter.hilbert_fc(65, window.WIN_HAMMING, 6.76)
        self.blocks_vector_to_stream_2_1_0 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_2_1 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_2_0_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_2_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_2_0 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_2 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_1_1_0 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_1_1 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_0_2_2 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_0_2_1_0 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_0_2_1 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_0_2 = blocks.vector_to_stream(gr.sizeof_float*1, line_length)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, ((line_length)*624))
        self.blocks_uchar_to_float_0_0_1 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_sub_xx_2_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_2 = blocks.sub_ff(1)
        self.blocks_sub_xx_0_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_streams_to_stream_0 = blocks.streams_to_stream(gr.sizeof_float*((line_length)*624), 3)
        self.blocks_stream_to_vector_2_1_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_2_1 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_2_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_2_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_2_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_2 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_0_2_0_1_0 = blocks.stream_to_vector(gr.sizeof_float*1, ((line_length)*624))
        self.blocks_stream_to_vector_0_2_0_1 = blocks.stream_to_vector(gr.sizeof_float*1, ((line_length)*624))
        self.blocks_stream_to_vector_0_2_0 = blocks.stream_to_vector(gr.sizeof_float*1, ((line_length)*624))
        self.blocks_stream_to_vector_0_1_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_0_0_1_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_0_0_1_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, line_length)
        self.blocks_stream_mux_1_0_0 = blocks.stream_mux(gr.sizeof_float*1, (line_length, 1))
        self.blocks_stream_mux_1_0 = blocks.stream_mux(gr.sizeof_float*1, (line_length, 1))
        self.blocks_stream_mux_1 = blocks.stream_mux(gr.sizeof_float*1, (line_length, 1))
        self.blocks_stream_mux_0_2 = blocks.stream_mux(gr.sizeof_float*1, (line_length2, sample_shift))
        self.blocks_stream_mux_0_1_0 = blocks.stream_mux(gr.sizeof_float*line_length, (1, 1))
        self.blocks_stream_mux_0_1 = blocks.stream_mux(gr.sizeof_float*line_length, (1, 1))
        self.blocks_stream_mux_0_0 = blocks.stream_mux(gr.sizeof_float*1, (line_length2, sample_shift))
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_float*line_length, (1, 1))
        self.blocks_stream_demux_2_1 = blocks.stream_demux(gr.sizeof_float*line_length, (312, 1))
        self.blocks_stream_demux_2_0 = blocks.stream_demux(gr.sizeof_float*line_length, (312, 1))
        self.blocks_stream_demux_2 = blocks.stream_demux(gr.sizeof_float*line_length, (312, 1))
        self.blocks_stream_demux_1_0_0 = blocks.stream_demux(gr.sizeof_float*line_length, (313, 312))
        self.blocks_stream_demux_1_0 = blocks.stream_demux(gr.sizeof_float*line_length, (313, 312))
        self.blocks_stream_demux_1 = blocks.stream_demux(gr.sizeof_float*line_length, (313, 312))
        self.blocks_stream_demux_0_1_2 = blocks.stream_demux(gr.sizeof_float*line_length, (lines_per_frame, lines_per_frame_discard))
        self.blocks_stream_demux_0_1 = blocks.stream_demux(gr.sizeof_float*line_length, (lines_per_frame, lines_per_frame_discard))
        self.blocks_repeat_0_0_2_0 = blocks.repeat(gr.sizeof_float*line_length, 2)
        self.blocks_repeat_0_0_2 = blocks.repeat(gr.sizeof_float*line_length, 2)
        self.blocks_null_sink_4_1 = blocks.null_sink(gr.sizeof_float*line_length)
        self.blocks_null_sink_4_0 = blocks.null_sink(gr.sizeof_float*line_length)
        self.blocks_null_sink_4 = blocks.null_sink(gr.sizeof_float*line_length)
        self.blocks_null_sink_0_1_2 = blocks.null_sink(gr.sizeof_float*line_length)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_float*line_length)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*line_length)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*line_length)
        self.blocks_multiply_const_vxx_2_0_0_0 = blocks.multiply_const_ff(.75)
        self.blocks_multiply_const_vxx_2_0_0 = blocks.multiply_const_ff(.75)
        self.blocks_multiply_const_vxx_2_0 = blocks.multiply_const_ff(.25)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_ff(.25)
        self.blocks_multiply_const_vxx_1_1 = blocks.multiply_const_ff(127)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_ff(180)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(127)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_ff(256)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(256)
        self.blocks_float_to_uchar_0_1 = blocks.float_to_uchar()
        self.blocks_float_to_uchar_0_0_0_0_1 = blocks.float_to_uchar()
        self.blocks_float_to_uchar_0_0_0 = blocks.float_to_uchar()
        self.blocks_float_to_uchar_0_0 = blocks.float_to_uchar()
        self.blocks_file_source_0_0_0 = blocks.file_source(gr.sizeof_char*1, inputdir + "/" + videofile + "_chroma.tbc", False, ((1135*626)*startfield), 0)
        self.blocks_file_source_0_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, inputdir + "/" + videofile + ".tbc", False, ((1135*626)*startfield), 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, outputdir + "/" + videofile + "_sf" + str(startfield) + ".bin", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_divide_xx_0_0 = blocks.divide_ff(1)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_float*1, colordelay)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, colordelay)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, (line_length+1))
        self.blocks_deinterleave_1_0_0 = blocks.deinterleave(gr.sizeof_float*line_length, 1)
        self.blocks_deinterleave_1_0 = blocks.deinterleave(gr.sizeof_float*line_length, 1)
        self.blocks_deinterleave_0_1 = blocks.deinterleave(gr.sizeof_float*1, 1)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_float*1, 1)
        self.blocks_add_xx_0_1 = blocks.add_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0_1_0 = blocks.add_const_ff(.6)
        self.blocks_add_const_vxx_0_1 = blocks.add_const_ff(1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff((-1))
        self.blocks_abs_xx_0_0 = blocks.abs_ff(1)
        self.blocks_abs_xx_0 = blocks.abs_ff(1)
        self.band_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                (round(samp_rate*1.0009)),
                (4406260-1000000),
                (4406260+1000000),
                100e3,
                window.WIN_KAISER,
                0))
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                (round(samp_rate*1.0009)),
                (4250000-1000000),
                (4250000+1000000),
                100e3,
                window.WIN_KAISER,
                0))
        self.analog_rail_ff_0_0_2 = analog.rail_ff(0, 255)
        self.analog_rail_ff_0_0_1 = analog.rail_ff((-1), 1)
        self.analog_rail_ff_0_0_0_1 = analog.rail_ff(0, 2)
        self.analog_rail_ff_0_0_0_0 = analog.rail_ff((-2), 0)
        self.analog_rail_ff_0_0_0 = analog.rail_ff((-1), 1)
        self.analog_rail_ff_0_0 = analog.rail_ff((-1), 1)
        self.analog_rail_ff_0 = analog.rail_ff((-1), 1)
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf((samp_rate/(2*math.pi*87500)))
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate/(2*math.pi*87500)))
        self.analog_fm_deemph_0_0 = analog.fm_deemph(fs=samp_rate, tau=fm_demph)
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=samp_rate, tau=fm_demph)
        self.analog_const_source_x_3_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, (-1))
        self.analog_const_source_x_3 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, (-1))
        self.analog_const_source_x_2_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_2_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_2 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_1_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, chroma_range_blue)
        self.analog_const_source_x_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, chroma_range_red)
        self.analog_const_source_x_0_1_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 32768)
        self.analog_const_source_x_0_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 32768)
        self.analog_const_source_x_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 32768)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 32768)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_sub_xx_2, 1))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_sub_xx_2_0, 1))
        self.connect((self.analog_const_source_x_0_1, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.analog_const_source_x_0_1_0, 0), (self.blocks_divide_xx_0_0, 1))
        self.connect((self.analog_const_source_x_1, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.analog_const_source_x_1_0, 0), (self.blocks_sub_xx_0_0, 1))
        self.connect((self.analog_const_source_x_2, 0), (self.blocks_stream_mux_1, 1))
        self.connect((self.analog_const_source_x_2_0, 0), (self.blocks_stream_mux_1_0, 1))
        self.connect((self.analog_const_source_x_2_0_0, 0), (self.blocks_stream_mux_1_0_0, 1))
        self.connect((self.analog_const_source_x_3, 0), (self.blocks_stream_mux_0_0, 1))
        self.connect((self.analog_const_source_x_3_0, 0), (self.blocks_stream_mux_0_2, 1))
        self.connect((self.analog_fm_deemph_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.analog_fm_deemph_0_0, 0), (self.blocks_multiply_const_vxx_2_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.analog_fm_deemph_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.analog_fm_deemph_0_0, 0))
        self.connect((self.analog_rail_ff_0, 0), (self.blocks_add_const_vxx_0_1_0, 0))
        self.connect((self.analog_rail_ff_0_0, 0), (self.blocks_stream_mux_0_2, 0))
        self.connect((self.analog_rail_ff_0_0_0, 0), (self.blocks_add_const_vxx_0_1, 0))
        self.connect((self.analog_rail_ff_0_0_0_0, 0), (self.blocks_abs_xx_0, 0))
        self.connect((self.analog_rail_ff_0_0_0_1, 0), (self.blocks_abs_xx_0_0, 0))
        self.connect((self.analog_rail_ff_0_0_1, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.analog_rail_ff_0_0_2, 0), (self.blocks_stream_mux_1, 0))
        self.connect((self.analog_rail_ff_0_0_2, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_abs_xx_0, 0), (self.blocks_delay_0_1, 0))
        self.connect((self.blocks_abs_xx_0_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.analog_rail_ff_0_0_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0_1, 0), (self.analog_rail_ff_0_0_0_1, 0))
        self.connect((self.blocks_add_const_vxx_0_1_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_sub_xx_2_0, 0))
        self.connect((self.blocks_add_xx_0_1, 0), (self.blocks_sub_xx_2, 0))
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_deinterleave_0_1, 0), (self.blocks_add_xx_0_1, 0))
        self.connect((self.blocks_deinterleave_0_1, 1), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_deinterleave_1_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.blocks_deinterleave_1_0, 1), (self.blocks_repeat_0_0_2_0, 0))
        self.connect((self.blocks_deinterleave_1_0_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_deinterleave_1_0_0, 0), (self.blocks_repeat_0_0_2, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_delay_0_1, 0), (self.blocks_multiply_const_vxx_1_1, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_stream_mux_0_0, 0))
        self.connect((self.blocks_divide_xx_0_0, 0), (self.analog_rail_ff_0_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_uchar_to_float_0_0, 0))
        self.connect((self.blocks_file_source_0_0_0, 0), (self.blocks_uchar_to_float_0_0_1, 0))
        self.connect((self.blocks_float_to_uchar_0_0, 0), (self.video_sdl_sink_0_0_0_0, 1))
        self.connect((self.blocks_float_to_uchar_0_0_0, 0), (self.video_sdl_sink_0_0_0_0, 0))
        self.connect((self.blocks_float_to_uchar_0_0_0_0_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_float_to_uchar_0_1, 0), (self.video_sdl_sink_0_0_0_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_add_xx_0_1, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_stream_mux_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.analog_rail_ff_0_0_2, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.blocks_stream_mux_1_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.qtgui_time_sink_x_0_0, 2))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0_0, 0), (self.blocks_stream_to_vector_0_0_1_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0_0_0, 0), (self.blocks_stream_to_vector_0_0_1_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0_0_0, 0), (self.qtgui_number_sink_1, 0))
        self.connect((self.blocks_repeat_0_0_2, 0), (self.blocks_vector_to_stream_0_2_1_0, 0))
        self.connect((self.blocks_repeat_0_0_2_0, 0), (self.blocks_vector_to_stream_0_2_1, 0))
        self.connect((self.blocks_stream_demux_0_1, 1), (self.blocks_null_sink_0_1, 0))
        self.connect((self.blocks_stream_demux_0_1, 0), (self.blocks_vector_to_stream_0_2, 0))
        self.connect((self.blocks_stream_demux_0_1_2, 1), (self.blocks_null_sink_0_1_2, 0))
        self.connect((self.blocks_stream_demux_0_1_2, 0), (self.blocks_vector_to_stream_0_2_2, 0))
        self.connect((self.blocks_stream_demux_1, 0), (self.blocks_stream_demux_2, 0))
        self.connect((self.blocks_stream_demux_1, 1), (self.blocks_vector_to_stream_2_0, 0))
        self.connect((self.blocks_stream_demux_1_0, 0), (self.blocks_stream_demux_2_0, 0))
        self.connect((self.blocks_stream_demux_1_0, 1), (self.blocks_vector_to_stream_2_0_0, 0))
        self.connect((self.blocks_stream_demux_1_0_0, 0), (self.blocks_stream_demux_2_1, 0))
        self.connect((self.blocks_stream_demux_1_0_0, 1), (self.blocks_vector_to_stream_2_0_0_0, 0))
        self.connect((self.blocks_stream_demux_2, 1), (self.blocks_null_sink_4, 0))
        self.connect((self.blocks_stream_demux_2, 0), (self.blocks_vector_to_stream_2, 0))
        self.connect((self.blocks_stream_demux_2_0, 1), (self.blocks_null_sink_4_0, 0))
        self.connect((self.blocks_stream_demux_2_0, 0), (self.blocks_vector_to_stream_2_1, 0))
        self.connect((self.blocks_stream_demux_2_1, 1), (self.blocks_null_sink_4_1, 0))
        self.connect((self.blocks_stream_demux_2_1, 0), (self.blocks_vector_to_stream_2_1_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.blocks_stream_mux_0_0, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_stream_mux_0_1, 0), (self.blocks_vector_to_stream_1_1, 0))
        self.connect((self.blocks_stream_mux_0_1_0, 0), (self.blocks_vector_to_stream_1_1_0, 0))
        self.connect((self.blocks_stream_mux_0_2, 0), (self.blocks_stream_to_vector_0_1_0, 0))
        self.connect((self.blocks_stream_mux_1, 0), (self.blocks_float_to_uchar_0_0_0, 0))
        self.connect((self.blocks_stream_mux_1_0, 0), (self.blocks_float_to_uchar_0_0, 0))
        self.connect((self.blocks_stream_mux_1_0_0, 0), (self.blocks_float_to_uchar_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_stream_demux_1, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_stream_demux_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_stream_demux_1_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_1_0_0_0, 0), (self.blocks_deinterleave_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_1_0_0_0_0, 0), (self.blocks_deinterleave_1_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.blocks_stream_demux_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_1_0, 0), (self.blocks_stream_demux_0_1_2, 0))
        self.connect((self.blocks_stream_to_vector_0_2_0, 0), (self.blocks_streams_to_stream_0, 0))
        self.connect((self.blocks_stream_to_vector_0_2_0_1, 0), (self.blocks_streams_to_stream_0, 1))
        self.connect((self.blocks_stream_to_vector_0_2_0_1_0, 0), (self.blocks_streams_to_stream_0, 2))
        self.connect((self.blocks_stream_to_vector_2, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_stream_to_vector_2_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_stream_to_vector_2_0_0, 0), (self.blocks_stream_mux_0_1, 1))
        self.connect((self.blocks_stream_to_vector_2_0_0_0, 0), (self.blocks_stream_mux_0_1_0, 1))
        self.connect((self.blocks_stream_to_vector_2_1, 0), (self.blocks_stream_mux_0_1, 0))
        self.connect((self.blocks_stream_to_vector_2_1_0, 0), (self.blocks_stream_mux_0_1_0, 0))
        self.connect((self.blocks_streams_to_stream_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_const_vxx_2_0_0_0, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.blocks_multiply_const_vxx_2_0_0, 0))
        self.connect((self.blocks_sub_xx_2, 0), (self.blocks_divide_xx_0_0, 0))
        self.connect((self.blocks_sub_xx_2_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.blocks_deinterleave_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0_1, 0), (self.blocks_deinterleave_0_1, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_float_to_uchar_0_0_0_0_1, 0))
        self.connect((self.blocks_vector_to_stream_0_2, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.blocks_vector_to_stream_0_2_1, 0), (self.analog_rail_ff_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_2_1_0, 0), (self.analog_rail_ff_0_0_1, 0))
        self.connect((self.blocks_vector_to_stream_0_2_2, 0), (self.hilbert_fc_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.blocks_stream_to_vector_0_2_0, 0))
        self.connect((self.blocks_vector_to_stream_1_1, 0), (self.blocks_stream_to_vector_0_2_0_1, 0))
        self.connect((self.blocks_vector_to_stream_1_1_0, 0), (self.blocks_stream_to_vector_0_2_0_1_0, 0))
        self.connect((self.blocks_vector_to_stream_2, 0), (self.blocks_stream_to_vector_2, 0))
        self.connect((self.blocks_vector_to_stream_2_0, 0), (self.blocks_stream_to_vector_2_0, 0))
        self.connect((self.blocks_vector_to_stream_2_0_0, 0), (self.blocks_stream_to_vector_2_0_0, 0))
        self.connect((self.blocks_vector_to_stream_2_0_0_0, 0), (self.blocks_stream_to_vector_2_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_2_1, 0), (self.blocks_stream_to_vector_2_1, 0))
        self.connect((self.blocks_vector_to_stream_2_1_0, 0), (self.blocks_stream_to_vector_2_1_0, 0))
        self.connect((self.hilbert_fc_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.hilbert_fc_0, 0), (self.band_pass_filter_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "secam2yuv")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_inputdir(self):
        return self.inputdir

    def set_inputdir(self, inputdir):
        self.inputdir = inputdir
        self.blocks_file_source_0_0.open(self.inputdir + "/" + self.videofile + ".tbc", False)
        self.blocks_file_source_0_0_0.open(self.inputdir + "/" + self.videofile + "_chroma.tbc", False)

    def get_outputdir(self):
        return self.outputdir

    def set_outputdir(self, outputdir):
        self.outputdir = outputdir
        self.blocks_file_sink_0.open(self.outputdir + "/" + self.videofile + "_sf" + str(self.startfield) + ".bin")

    def get_startfield(self):
        return self.startfield

    def set_startfield(self, startfield):
        self.startfield = startfield
        self.blocks_file_sink_0.open(self.outputdir + "/" + self.videofile + "_sf" + str(self.startfield) + ".bin")

    def get_videofile(self):
        return self.videofile

    def set_videofile(self, videofile):
        self.videofile = videofile
        self.blocks_file_sink_0.open(self.outputdir + "/" + self.videofile + "_sf" + str(self.startfield) + ".bin")
        self.blocks_file_source_0_0.open(self.inputdir + "/" + self.videofile + ".tbc", False)
        self.blocks_file_source_0_0_0.open(self.inputdir + "/" + self.videofile + "_chroma.tbc", False)

    def get_sample_shift(self):
        return self.sample_shift

    def set_sample_shift(self, sample_shift):
        self.sample_shift = sample_shift
        self.set_colordelay(1070+self.sample_shift)
        self.set_line_length(self.line_length2+self.sample_shift)

    def get_line_length2(self):
        return self.line_length2

    def set_line_length2(self, line_length2):
        self.line_length2 = line_length2
        self.set_line_length(self.line_length2+self.sample_shift)

    def get_startfield_old(self):
        return self.startfield_old

    def set_startfield_old(self, startfield_old):
        self.startfield_old = startfield_old

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*math.pi*87500)))
        self.analog_quadrature_demod_cf_0_0.set_gain((self.samp_rate/(2*math.pi*87500)))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, (round(self.samp_rate*1.0009)), (4250000-1000000), (4250000+1000000), 100e3, window.WIN_KAISER, 0))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, (round(self.samp_rate*1.0009)), (4406260-1000000), (4406260+1000000), 100e3, window.WIN_KAISER, 0))
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_lines_per_frame_discard(self):
        return self.lines_per_frame_discard

    def set_lines_per_frame_discard(self, lines_per_frame_discard):
        self.lines_per_frame_discard = lines_per_frame_discard

    def get_lines_per_frame(self):
        return self.lines_per_frame

    def set_lines_per_frame(self, lines_per_frame):
        self.lines_per_frame = lines_per_frame

    def get_line_length(self):
        return self.line_length

    def set_line_length(self, line_length):
        self.line_length = line_length
        self.blocks_delay_0.set_dly(int((self.line_length+1)))

    def get_fm_demph(self):
        return self.fm_demph

    def set_fm_demph(self, fm_demph):
        self.fm_demph = fm_demph

    def get_colordelay(self):
        return self.colordelay

    def set_colordelay(self, colordelay):
        self.colordelay = colordelay
        self.blocks_delay_0_0.set_dly(int(self.colordelay))
        self.blocks_delay_0_1.set_dly(int(self.colordelay))

    def get_chroma_range_red(self):
        return self.chroma_range_red

    def set_chroma_range_red(self, chroma_range_red):
        self.chroma_range_red = chroma_range_red
        self.analog_const_source_x_1.set_offset(self.chroma_range_red)

    def get_chroma_range_blue(self):
        return self.chroma_range_blue

    def set_chroma_range_blue(self, chroma_range_blue):
        self.chroma_range_blue = chroma_range_blue
        self.analog_const_source_x_1_0.set_offset(self.chroma_range_blue)



def argument_parser():
    description = 'Takes luma and secam chroma TBC files and generates YUV file'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--inputdir", dest="inputdir", type=str, default='/home/user/input/',
        help="Set inputdir [default=%(default)r]")
    parser.add_argument(
        "--outputdir", dest="outputdir", type=str, default='/home/user/output/',
        help="Set outputdir [default=%(default)r]")
    parser.add_argument(
        "--startfield", dest="startfield", type=intx, default=0,
        help="Set startfield [default=%(default)r]")
    parser.add_argument(
        "--videofile", dest="videofile", type=str, default='tbcfilename',
        help="Set videofile [default=%(default)r]")
    return parser


def main(top_block_cls=secam2yuv, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(inputdir=options.inputdir, outputdir=options.outputdir, startfield=options.startfield, videofile=options.videofile)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
