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

    place_names = {}
    places = []

    for name, attr in NETS[SCHEMA]['places'].items():
        place_names[attr['offset']] = name
        el = place(attr['position'][0] * scale, attr['position'][1] * scale, label=name)
        places.append(el)

    arc_defs = {}
    transitions = []
    _size = len(place_names)

    for name, attr in NETS[SCHEMA]['transitions'].items():
        if name not in arc_defs:
            arc_defs[name] = { 'to': [], 'from': [] }

        for i in range(0, _size):
            if attr['delta'][i] > 0:
                arc_defs[name]['to'].append(place_names[i])

            elif attr['delta'][i] < 0:
                arc_defs[name]['from'].append(place_names[i])

        el = transition(attr['position'][0] * scale, attr['position'][1] * scale, label=name)
        transitions.append(el)

    # draw places
    for pl in places:

        _handle(
            x=float(pl.node.attributes.x2.value),
            y=float(pl.node.attributes.y2.value),
            refid=pl.data('label'),
            symbol='place'
        )

    # draw transitions
    for tx in transitions:
        _handle(
            x=float(tx.node.attributes.x2.value),
            y=float(tx.node.attributes.y2.value),
            refid=pl.data('label'),
            symbol='transition'
        )

    # draw arcs
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
    x1 = float(_attr(sym1).x2.value)
    y1 = float(_attr(sym1).y2.value)
    x2 = float(_attr(sym2).x2.value)
    y2 = float(_attr(sym2).y2.value)

    if SYMBOLS[sym2].data('symbol') == 'place':
        start='transition'
        end='place'
    else:
        end='transition'
        start='place'

    _id = '%s-%s' % (sym1, sym2)
    el = _arc(x1, y1, x2, y2, refid=_id, start=start, end=end)
    el.data('symbol', 'arc')
    el.data('start', sym1)
    el.data('end', sym2)

    return el

def _load_symbols():
    """ use snap to generate the symbols needed to render a petri-net """
    window.SYMBOLS = SYMBOLS
    SYMBOLS['arrow'] = _arrow()

def _node(x, y, label=None, symbol=None):
    """ adds a petri-net symbol to the graph """

    point_el= _point(x=x, y=y, refid=label)
    point_el.data('symbol', symbol)
    point_el.data('label', label)

    SYMBOLS[label] = point_el
    return point_el

def _attr(sym):
    """ access attributes of an existing symbol """
    return SYMBOLS[sym].node.attributes

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


def _arc(x1, y1, x2, y2, weight=1, refid=None, start=None, end=None):

    if start == 'place':
        if x1 > x2:
            x1 = x1 - 20 
            x2 = x2 + 10
        else:
            x1 = x1 + 20
            x2 = x2 - 10

    if end == 'place':
        if x1 > x2:
            x1 = x1 - 5 
            x2 = x2 + 20
        else:
            x1 = x1 + 5
            x2 = x2 - 20
    
    el = PAPER.line({
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
    }).attr({
        'id': refid,
        'class': 'arc',
        'stroke': '#000',
        'stroke-opacity': '0.8',
        'strokeWidth': 1,
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

def _handle(x=0, y=50, size=40, capacity=0, refid=None, symbol=None):
    """ add element for UI interaction """
    _id = refid + '-handle'

    if symbol == 'place':
        el = PAPER.circle({
            'cx': x,
            'cy': y,
            'r': (size/2)
        }).attr({
            'id': _id,
            'class': symbol,
            'fill': '#FFF',
            'fill-opacity': 1,
            'stroke': '#000',
            'orient': 0 
        })

    else:
        el = PAPER.rect({
            'x': x - 5,
            'y': y - 17,
            'width': 10,
            'height': 34,
        }).attr({
            'id': _id,
            'class': symbol,
            'fill': '#000',
            'fill-opacity': 1,
            'stroke': '#000',
            'strokeWidth': 2,
            'orient': 0 
        })

    el.data('refid', refid)
    SYMBOLS[_id] = el

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
