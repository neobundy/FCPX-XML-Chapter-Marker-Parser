#!/usr/bin/env python3
# Wankyu Choi - Creative Works of Knowledge 2019
#
# Final Cut XML Chapter Marker Parser is free software: you can use it, redistribute it and/or modify it under the terms of the GNU General Public License (GPL) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# Final Cut XML Chapter Marker Parser is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GNU General Public License for more details.

#
# Final Cut XML Chapter Marker Parser for YouTube Timestamp Links
#
# Automagically turns FCPX chapter markers into a list of YouTube timestamp links.
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

        # only picks up chapter markers
        # example:
        #  <chapter-marker start="29100071/8000s" duration="1001/24000s" value="Chapter 1" posterOffset="11/24s"/>

        if 'chapter-marker' == element.tag:
            m.append(Marker(element.attrib['value'], start + sum(time)))

        # sums up the offset from the other tags
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

        # a dictionary is used to leave only the final (unique) chapter markers

        marker_dict = {}
        for m in markers:
            # we don't need the trailing frame part for youtube timestamp links, hence the split('.')

            try:
                marker_dict[m.name], frame = str(datetime.timedelta(seconds=m.start_time)).split('.')
            except ValueError:
                marker_dict[m.name] = str(datetime.timedelta(seconds=m.start_time))

        for name, start_time in marker_dict.items():
            print("{} {}".format(name, start_time))

if __name__ == '__main__':
    main()
