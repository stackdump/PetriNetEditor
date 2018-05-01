import re
import json
from browser import window, document as doc
from browser import websocket, ajax, console

_SEQ = 0
_CFG = None
_ENDPOINT = ''

def __onload(config):
    """
    config is requested and this method is
    called as this module is included  (see bottom of file)
    """
    global _CFG
    global _ENDPOINT
    _CFG = config
    _ENDPOINT = _CFG['endpoint']

def _get(resource, callback=None, errback=None):
    """ _get(resource, callback=None, errback=None): make http GET to backend """
    req = ajax.ajax()
    if callback:
        req.bind('complete', callback)
    else:
        req.bind('complete', echo)
    req.open('GET', _ENDPOINT + resource, True)
    req.send()

def echo(req):
    """ echo(req): append return value to terminal as an assignment to a var: '_' """
    doc['code'].value += "\n_ = " + req.response

def machine(schema, callback=None):
    """ machine(schema, callback=None): get machine definition """
    _get('/machine/%s' % schema, callback=callback)
