import json
from browser import window, document
from browser import ajax, console
from controller import Controller
from editor import Editor
from importer import Importer

class Context(object):
    """ application context object provides an interface to server-side api calls """

    def __init__(self):
        self.seq = 0
        self.endpoint = ''
        self.log = console.log
        self._get(window.Bitwrap.config, self.configure)
        self.doc = document

    def time(self):
        """ return time in microseconds """
        return window.Date.now()

    def configure(self, req):
        """ load config from server """
        _config = json.loads(req.text)
        self.endpoint = _config['endpoint']
        _editor = Editor(context=self, config=_config)

        Controller(context=self, editor=_editor)

    @staticmethod
    def echo(req):
        """ write return value to console """
        try:
            txt = getattr(req, 'response')
            console.log(txt)
        except:
            console.log(req)

    @staticmethod
    def clear(txt=''):
        """ clear python terminal """
        document['code'].value = txt

    def _get(self, resource, callback=None, errback=None):
        """ _get(resource, callback=None, errback=None): make http GET to backend """
        req = ajax.ajax()
        if callback:
            req.bind('complete', callback)
        else:
            req.bind('complete', self.echo)
        req.open('GET', self.endpoint + resource, True)
        req.send()

    def schemata(self, callback=None):
        """ schemata(callback=None): retrieve list of available state machine definitions """
        self._get('/schemata/index.xml', callback=callback)

    def machine(self, schema, callback=None):
        """ machine(schema, callback=None): get machine definition """

        def _callback(req):
            import_net = Importer(req.text)
            # KLUDGE: stuff json response into response - editor re-parses json
            req.text=json.dumps(import_net.from_xml())

            if callable(callback):
                callback(req)

        self._get('/schemata/%s.xml' % schema, callback=_callback)
