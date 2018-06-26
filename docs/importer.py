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

    @staticmethod
    def _position(el):
        pos = el.getElementsByTagName('position')[0]
        return [pos.x, pos.y]

    @staticmethod
    def _initial(el):
        mark = el.getElementsByTagName('initialMarking')[0]
        val_el = mark.getElementsByTagName('value')[0]
        val = val_el.text.split(',')
        assert val[0] == 'Default' # only support 1 color token
        return int(val[1])

    @staticmethod
    def _weight(el):
        inscription = el.getElementsByTagName('inscription')[0]
        val_el = inscription.getElementsByTagName('value')[0]
        val = val_el.text.split(',')
        assert val[0] == 'Default' # only support 1 color token
        return int(val[1])

    def _offset(self, place_id):
        if place_id not in self.instance['machine']['places']:
            return None

        return self.instance['machine']['places'][place_id]['offset']

    def from_xml(self):
        parser = window.DOMParser.new()
        doc = parser.parseFromString(self.raw, "application/xml");

        for offset, place in enumerate(doc.getElementsByTagName('place')):
            self.instance['machine']['places'][place.id] = {
                "initial": self._initial(place),
                "offset": offset,
                "position": self._position(place)
            }

        for transition in doc.getElementsByTagName('transition'):
            self.instance['machine']['transitions'][transition.id] = {
                "delta": [0] * len(self.instance['machine']['places']),
                "position": self._position(transition)
            }

        for arc in doc.getElementsByTagName('arc'):
            _source_idx = self._offset(arc.source)
            _target_idx = self._offset(arc.target)

            if _target_idx is None:
                txn = arc.target
                sign = -1
                offset = _source_idx
            else:
                txn = arc.source
                sign = 1
                offset = _target_idx

            delta_val = sign * self._weight(arc)

            self.instance['machine']['transitions'][txn]['delta'][offset] += delta_val

        return self.instance

