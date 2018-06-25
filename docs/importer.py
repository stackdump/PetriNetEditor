""" Export Petri-Net as xml/PNML """

from browser import window, console

class Importer(object):

    def __init__(self, xml_str):
        self.raw = xml_str
        self.instance = {
            "machine": {
                "name": "",
                "places": {},
                "transitions": {}
            }
        }

    @staticmethod
    def parse_file_list(xml_str):
        """ read schema index and return list of files """
        parser = window.DOMParser.new()
        doc = parser.parseFromString(xml_str, "application/xml");
        _list = [ pnml_file.name[:-4] for pnml_file in doc.getElementsByTagName('file') ]

        return { 'schemata': _list }

    def from_xml(self):
        parser = window.DOMParser.new()
        doc = parser.parseFromString(self.raw, "application/xml");
        console.log('--parser--')
        console.log(doc)

        return self.instance

