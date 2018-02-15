from browser import window, document, console
import json

PAPER = None
"""
Snap.svg instance
"""

NETS = {}
"""
petr-net definitions
"""

SYMBOLS = {}
"""
svg graphic elements used to render a Petri-Net
"""

SCHEMA = None
"""
petri-net in use
"""

def __onload(ctx):
    """ use snap to begin creating an SVG """
    ctx.machine('octoe', callback=load)

def reset():
    """ clear SVG and prepare markers """
    global PAPER
    
    if not PAPER:
        PAPER=window.Snap('#net')

    PAPER.clear()
    _load_symbols()
    _origin()

def load(res):
    """ store requested PNML and render as SVG """
    global SCHEMA

    pnet  = json.loads(res.text)
    SCHEMA = pnet['machine']['name']
    NETS[SCHEMA] = pnet['machine']
    reload()

def reload():
    """ reset then render """
    reset()
    render()

def render(scale=1.3):
    """ development examples """

    place_defs = {}

    for name, attr in NETS[SCHEMA]['places'].items():
        place_defs[attr['offset']] = name
        place(attr['position'][0] * scale, attr['position'][1] * scale, label=name)

    arc_defs = {}
    _size = len(place_defs)

    for name, attr in NETS[SCHEMA]['transitions'].items():
        if name not in arc_defs:
            arc_defs[name] = { 'to': [], 'from': [] }

        for i in range(0, _size):
            if attr['delta'][i] > 0:
                arc_defs[name]['to'].append(place_defs[i])

            elif attr['delta'][i] < 0:
                arc_defs[name]['from'].append(place_defs[i])

        transition(attr['position'][0] * scale, attr['position'][1] * scale, label=name)

    for txn, attrs in arc_defs.items():
        if attrs['to']:
            for label in attrs['to']:
                arc(txn, label)

        if attrs['from']:
            for label in attrs['from']:
                arc(label, txn)

def place(x, y, label=None):
    """ adds a place node """
    return _node(x, y, label=label, symbol='place')

def transition(x, y, label=None):
    """ adds a transition node """
    return _node(x, y, label=label, symbol='transition')

def arc(sym1, sym2, token_weight=1):
    """ draw arc between 2 points """
    x1 = _attr(sym1).x2.value
    y1 = _attr(sym1).y2.value
    x2 = _attr(sym2).x2.value
    y2 = _attr(sym2).y2.value

    _id = '%s-%s' % (sym1, sym2)
    el = _arc(x1, y1, x2, y2, arcid=_id)
    el.data('symbol', 'arc')
    el.data('start', sym1)
    el.data('end', sym2)

    return el

def _load_symbols():
    """ use snap to generate the symbols needed to render a petri-net """
    window.SYMBOLS = SYMBOLS
    SYMBOLS['arrow'] = _arrow()
    SYMBOLS['place'] = _place()
    SYMBOLS['transition'] = _transition()

def _node(x, y, label=None, symbol=None):
    """ adds a petri-net symbol to the graph """
    handle_id = '%s-handle' % label

    point_el= _point(x=x, y=y, refid=label)
    point_el.data('symbol', symbol)
    point_el.data('handle', handle_id)
    point_el.attr({ 'markerEnd': SYMBOLS[symbol] })

    handle_el = _handle(x,y, refid=handle_id)
    handle_el.data('label', label)

    SYMBOLS[label] = point_el
    return point_el

def _attr(sym):
    """ access attributes of an existing symbol """
    return SYMBOLS[sym].node.attributes

def _arc(x1, y1, x2, y2, arcid=None):
    """ render line with arrowhead between 2 points """
    el = _arrowhead(x1, y1, x2, y2, refid=arcid)
    SYMBOLS[arcid] = el
    return el

def _origin(x1=0, y1=0, x2=100, y2=100):
    PAPER.line({
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

    PAPER.line({
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

def _point(x=0, y=0, refid=None):

    el = PAPER.line({
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

    SYMBOLS[refid] = el
    return el


def _arrowhead(x1, y1, x2, y2, weight=1, refid=None):
    el = PAPER.line({
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

    SYMBOLS[refid] = el
    return el

def _arrow():
    """ arrow head """
    return PAPER.path(
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

def _handle(x=0, y=50, size=90, capacity=0, refid=None):
    """ add element for UI interaction """

    el = PAPER.circle({
        'cx': x,
        'cy': y,
        'r': (size/2)
    }).attr({
        'id': refid,
        'class': 'handle',
        'fill': '#facade',
        'fill-opacity': '0.5',
        'stroke': '#facade',
        'orient': 0 
    })

    SYMBOLS[refid] = el

    def _drag_start(*args):
        # TODO redraw element
        console.log(args)

    def _drag_end(*args):
        # TODO redraw element
        reload()
        console.log(args)

    def _move(dx, dy, x, y, event):
        _tx = 't %i %i' % (dx, dy)
        el.transform(_tx)
    
    el.drag(_move, _drag_start, _drag_end)

    return el

def _place(x=25, y=50, size=30, capacity=0):
    """ add place to petri-net """

    return PAPER.circle({
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

    return PAPER.rect({
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
