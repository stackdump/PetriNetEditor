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

    ## development examples ##
    _origin()

    place(225,200, label='foo')
    place(225,300, label='qux')
    place(225,400, label='wolf')
    place(400,550, label='wang')

    transition(400,250, label='bar')
    transition(400,350, label='baz')
    transition(400,450, label='gang')
    transition(225,500, label='golf')

    arc('foo', 'bar')
    arc('bar', 'qux')
    arc('qux', 'baz')
    arc('baz', 'wolf')
    arc('wolf', 'gang')
    arc('gang', 'wang')
    arc('wang', 'golf')
    arc('golf', 'wolf')

def place(x, y, label=None):
    """ adds a place symbol """
    _node(x, y, label=label, symbol='place')

def transition(x, y, label=None):
    """ adds a transition symbol """
    _node(x, y, label=label, symbol='transition')

def _node(x, y, label=None, symbol=None):
    """ adds a petri-net symbol to the graph """
    point_id = _uniqueid()
    element = _point(x=x, y=y, refid=point_id)
    element.data('symbol', symbol)

    element.attr({ 'markerEnd': SYMBOLS[symbol] })
    SYMBOLS[label] = element
    return element

def arc(sym1, sym2, token_weight=1):
    """ draw arc between 2 symbols """
    x1 = SYMBOLS[sym1].node.attributes.x2.value
    y1 = SYMBOLS[sym1].node.attributes.y2.value
    x2 = SYMBOLS[sym2].node.attributes.x2.value
    y2 = SYMBOLS[sym2].node.attributes.y2.value

    _id = '%s-%s' % (sym1, sym2)
    element = _arc(x1, y1, x2, y2, arcid=_id)

    return element

def _arc(x1, y1, x2, y2, arcid=None):
    """ render line with arrowhead between 2 points """

    _handle(x1,y1, refid=arcid, marker='start')
    _handle(x2,y2, refid=arcid, marker='end')

    element = _arrowhead(x1, y1, x2, y2, refid=arcid)
    element.data('symbol', 'arc')
    element.data('start', sym1)
    element.data('end', sym2)

    SYMBOLS[arcid] = element

    return element

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
        #'stroke': '#87CDDE',
        'strokeWidth': 2
    })

    element.data('coords', [x, y])

    SYMBOLS[refid] = element
    return element


def _arrowhead(x1, y1, x2, y2, weight=1, refid=None):
    element = _PAPER.line({
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
    }).attr({
        'id': refid,
        'class': 'arc',
        'stroke': '#000',
        'strokeWidth': 2,
        'markerEnd': SYMBOLS['arrow']
    })

    SYMBOLS[refid] = element
    return element

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
        'fill-opacity': '0.5',
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
