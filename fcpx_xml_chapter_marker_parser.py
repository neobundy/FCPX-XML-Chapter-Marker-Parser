#!/usr/bin/env python3
# Wankyu Choi - Creative Works of Knowledge 2019
# https://www.youtube.com/wankyuchoi
#

import sys, datetime
from xml.etree.ElementTree import parse

def convert_fcp_time_string (fcp_time_string):
    """
    Converts 64/32 bit time string format into seconds
    example: 9256247/2400s
    """

    vals = fcp_time_string.replace('s', '').split('/')

    return float(vals[0]) / float(vals[1])

class Marker:
    def __init__(self, name, start_time):
        self._name = name
        self._start_time = start_time

    @property
    def start_time(self):
        return self._start_time

    @property
    def name(self):
        return self._name

    @staticmethod
    def find_chapter_marker(element, time=[]):
        start = offset = 0
        try:
            start = convert_fcp_time_string(element.attrib['start'])
        except:
            pass

        try:
            offset = convert_fcp_time_string(element.attrib['offset'])
        except:
            pass

        m = []
        if 'chapter-marker' == element.tag:
            m.append(Marker(element.attrib['value'], start + sum(time)))
        else:
            time.append(offset - start)
            for el in element:
                m.extend(Marker.find_chapter_marker(el, list(time)))
        return m


def main():

    # Usage:
    #    python fcpx_xml_chapter_marker_parser.py your_fcpx_xml_export_path

    # xml_file should point to your FCPX XMLexport file
    # this script only picks up chapter-markers

    try:
        xml_file = sys.argv[1]
    except IndexError:

        print("Usage: python fcpx_xml_chapter_marker_parser.py your_fcpx_xml_export_path")

    else:

        xmlroot = parse(xml_file).getroot()

        markers = sorted(Marker.find_chapter_marker(xmlroot), key=lambda s: s.start_time)

        marker_dict = {}

        for m in markers:
            marker_dict[m.name], frame = str(datetime.timedelta(seconds=m.start_time)).split('.')

        for name, start_time in marker_dict.items():
            print("{} {}".format(name, start_time))

if __name__ == '__main__':
    main()
