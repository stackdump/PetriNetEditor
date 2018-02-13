from browser import window, document, console

_PAPER = None
"""
Snap.svg instance
"""

SYMBOLS = {}
"""
graphic elements used to render a Petri-Net
"""

__IDX = 0

def _uniqueid():
    global __IDX
    __IDX = __IDX + 1

    return 'idx%i' % __IDX

def __onload():
    """ use snap to begin creating an SVG """

    global _PAPER
    _PAPER=window.Snap('#net')
    __load_symbols()

def __load_symbols():
    """ use snap to generate the symbols needed to render a petri-net """
    window.SYMBOLS = SYMBOLS
    SYMBOLS['arrow'] = _arrow()
    SYMBOLS['place'] = _place()
    SYMBOLS['transition'] = _transition()
    SYMBOLS['none'] = None #FIXME_transition()

    # for development render examples
    _origin()

    point_id = _uniqueid()
    _point(x=100, y=100, refid=point_id)

    arc(225,200, 400,250, start='place', end='transition')
    arc(400,350, 225,300, start='transition', end='place')

    arc(225,400, 400,450, start='transition', end='place')
    arc(400,550, 225,500, start='place', end='transition')


def arc(x1, y1, x2, y2, start=None, end=None, token_weight=1):
    """ add place to petri-net """
    arcid = _uniqueid()

    _handle(x1,y1, refid=arcid, marker='start')
    _handle(x2,y2, refid=arcid, marker='end')

    _attrs = {
        'id': arcid,
        'class': 'arc',
        'stroke': 'none',
        'strokeWidth': 2,
        'markerStart': SYMBOLS[start],
        'markerEnd': SYMBOLS[end]
    }

    element = _PAPER.line({
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
    }).attr(_attrs)

    _arrowhead(x1, y1, x2, y2, refid=arcid)

    SYMBOLS[arcid] = element

def _origin(x1=0, y1=0, x2=100, y2=100):
    x_arrow = _PAPER.line({
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': 0,
    }).attr({
        'id': 'origin_x',
        'class': 'origin',
        'stroke': '#000',
        'strokeWidth': 2,
        'markerEnd': SYMBOLS['arrow']
    })

    y_arrow = _PAPER.line({
        'x1': x1,
        'y1': y1,
        'x2': 0,
        'y2': y2,
    }).attr({
        'id': 'origin_y',
        'class': 'origin',
        'stroke': '#000',
        'strokeWidth': 2,
        'markerEnd': SYMBOLS['arrow']
    })

    SYMBOLS['origin_x'] = x_arrow
    SYMBOLS['origin_y'] = y_arrow

def _point(x=0, y=0, refid=None):

    element = _PAPER.line({
        'x1': 0,
        'y1': 0,
        'x2': x,
        'y2': y,
    }).attr({
        'id': refid,
        'class': 'point',
        'stroke': '#000',
        'strokeWidth': 2
    })

    element.data('coords', [x, y])

    SYMBOLS[refid] = element
    return element


def _arrowhead(x1, y1, x2, y2, weight=1, refid=None):
    arrowid = '%s-arrow' % refid

    element = _PAPER.line({
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
    }).attr({
        'id': arrowid,
        'class': 'arc',
        'stroke': '#000',
        'strokeWidth': 2,
        'markerEnd': SYMBOLS['arrow']
    })

    SYMBOLS[arrowid] = element

def _arrow():
    """ arrow head """
    return _PAPER.path(
        "M 2 59 L 293 148 L 1 243 L 121 151 Z"
    ).marker({
        'x': 0,
        'y': 0,
        'width': 8000,
        'height': 8000,
        'refX': 260,
        'refY': 150
    }).attr({
        'fill':'white',
        'stroke': 'black',
        'strokeWidth': 10,
        'markerUnits':'strokeWidth',
        'markerWidth': 350,
        'markerHeight':350,
        'orient': "auto" 
    })

def _handle(x=0, y=50, size=90, capacity=0, refid=None, marker=None):
    """ add element for UI interaction """

    handle_id = '%s-%s' % (refid, marker)

    element = _PAPER.circle({
        'cx': x,
        'cy': y,
        'r': (size/2)
    }).attr({
        'id': handle_id,
        'class': 'handle',
        'fill': '#facade',
        'fill-opacity': '1',
        'stroke': '#facade',
        'orient': 0 
    })

    SYMBOLS[handle_id] = element

    def _drag_start(*args):
        # TODO redraw element
        console.log(args)

    def _drag_end(*args):
        # TODO redraw element
        console.log(args)

    def _move(dx, dy, x, y, event):
        _tx = 't %i %i' % (dx, dy)
        element.transform(_tx)
    
    if marker == 'start':
       element.drag(_move, _drag_start, _drag_end)

    if marker == 'end':
       element.drag(_move, _drag_start, _drag_end)

    return element

def _place(x=25, y=50, size=30, capacity=0):
    """ add place to petri-net """

    return _PAPER.circle({
        'cx': x,
        'cy': y,
        'r': (size/2)
    }).marker({
        'x': 0,
        'y': 0,
        'width': 500,
        'height': 500,
        'refX': x + size/2,
        'refY': 50
    }).attr({
        'class': 'place',
        'fill': '#facade',
        'fill-opacity': '0',
        'stroke': '#000',
        'strokeWidth': 4,
        'markerUnits':'strokeWidth',
        'markerWidth': 350,
        'markerHeight':350,
        'orient': 0 
    })
    
def _transition(x=14, y=20, width=14, height=40, rx=0, ry=0):
    """ add transition to petri-net """

    return _PAPER.rect({
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        'rx': rx,
        'ry': ry
    }).marker({
        'x': 0,
        'y': 0,
        'width': 500,
        'height': 500,
        'refX': x,
        'refY': y + height/2
    }).attr({
        'class': 'transition',
        'fill': '#facade',
        'fill-opacity': '0',
        'stroke': '#000',
        'strokeWidth': 4,
        'markerUnits':'strokeWidth',
        'markerWidth': 350,
        'markerHeight':350,
        'orient': 0 
    })
