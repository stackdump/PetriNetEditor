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

INSTANCE = None
"""
elements and network state
"""

CTL = None
"""
UI control interface
"""

def __onload(ctx):
    """ use snap to begin creating an SVG """
    global CTL
    CTL = Control()

    ctx.machine('octoe', callback=load)
    window.jQuery('.ctl').on('click', CTL.handler)

class Control(object):
    """ Provide interface for UI actions """

    def __init__(self):
        self.selected = None

        self.commands = {
            'place': self.place,
            'transition': self.transition,
            'arc': self.arc,
            'select': self.select,
            '+token': self.inc_token,
            '-token': self.dec_token,
            'exec': self.start,
            'halt': self.stop
        }

    def handler(self, event):
        """ map input event to function call """
        try:
            cmd = str(event.target.text)
            _call = self.commands[cmd]
            self.selected = cmd
            _call(event)
        except:
            console.log('ctl_error', event)

    def log(self, event):
        """ log event to console """
        console.log(event.target.text)

    def place(self, event):
        """ add a place on every click """
        self.log(event)

    def transition(self, event):
        """ add a transtion on every click """
        self.log(event)

    def arc(self, event):
        """
        operate as a 'selector'
        where an arc is drawn between start/end clicks

        NOTE: only valid if start and end are different types place/transion
        """
        self.log(event)

    def select(self, event):
        """ select an item to edit """
        self.log(event)

    def inc_token(self, event):
        """ add 1 token from inital marking """
        # REVIEW: ? should this work on arcs also?
        self.log(event)

    def dec_token(self, event):
        """ remove 1 token from inital marking """
        # REVIEW: ? should this work on arcs also?
        self.log(event)

    def start(self, event):
        """ start the simulator """
        # TODO:
        # 1. reindex allowable actions for INSTANCE
        # 2. hilight 'live' transitions
        self.log(event)

    def stop(self, event):
        """ stop the simulator """
        self.log(event)


def load(res):
    """ store requested PNML and render as SVG """
    global SCHEMA

    pnet  = json.loads(res.text)
    SCHEMA = pnet['machine']['name']
    NETS[SCHEMA] = pnet['machine']
    reset(callback=render)

def reset(callback=None):
    """ clear SVG and prepare markers """
    global PAPER
    
    if not PAPER:
        PAPER=window.Snap('#net')

    PAPER.clear()
    _load_symbols()
    _origin()

    if callback:
        callback()

def render():
    """ development examples """
    global INSTANCE

    if not INSTANCE:
        INSTANCE = PNet()

    INSTANCE.render()

class PNet(object):

    def __init__(self):
        """ persistent net object """

        self.places = {}
        self.place_names = {}
        self.place_defs = {}

        self.token_ledger = {}

        self.arcs = []
        self.arc_defs = {}

        self.transition_defs = {}
        self.transitions = {}

        self.handles = []
        self.reindex()
        self.vector_size = 0

    def reindex(self):
        """ rebuild data points """

        for name, attr in NETS[SCHEMA]['places'].items():
            self.place_names[attr['offset']] = name
            self.place_defs[name] = attr

        self.vector_size = len(self.place_names)

        for name, attr in NETS[SCHEMA]['transitions'].items():
            if name not in self.arc_defs:
                self.arc_defs[name] = { 'to': [], 'from': [] }

            for i in range(0, self.vector_size):
                if attr['delta'][i] > 0:
                    self.arc_defs[name]['to'].append(self.place_names[i])

                elif attr['delta'][i] < 0:
                    self.arc_defs[name]['from'].append(self.place_names[i])

            self.transition_defs[name] = { 'position': attr['position'] }

    def render(self):
        """ draw the petri-net """
        self.render_nodes()
        self.render_handles()
        self.render_arcs()

    def render_nodes(self):
        """ draw points used to align other elements """

        for name, attr in self.place_defs.items():
            self.token_ledger[name] = attr['inital']

            el = place(attr['position'][0], attr['position'][1], label=name)
            el.data('offset', attr['offset'])
            el.data('inital', attr['inital']) 
            el.data('tokens', attr['inital'])
            self.places[name] = el

        for name, attr in self.transition_defs.items():
            el = transition(attr['position'][0], attr['position'][1], label=name)
            self.transitions[name] = el

    def render_handles(self):
        """ draw places and transitions """

        for _, pl in self.places.items():
            el = _handle(
                x=float(pl.node.attributes.x2.value),
                y=float(pl.node.attributes.y2.value),
                refid=pl.data('label'),
                symbol='place'
            )
            self.handles.append(el)

        for _, tx in self.transitions.items():
            el = _handle(
                x=float(tx.node.attributes.x2.value),
                y=float(tx.node.attributes.y2.value),
                refid=tx.data('label'),
                symbol='transition'
            )
            self.handles.append(el)

    def render_arcs(self):
        """ draw the petri-net """

        for txn, attrs in self.arc_defs.items():

            if attrs['to']:
                for label in attrs['to']:
                    el = arc(txn, label)
                    self.arcs.append(el)

            if attrs['from']:
                for label in attrs['from']:
                    el = arc(label, txn)
                    self.arcs.append(el)


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
    """ draw x/y axis """

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
    """ draw hidden point """

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
    """
    draw arc with arrow
    This also adjusts x coordintates to match place/transition size
    """

    if start == 'place':
        if x1 > x2:
            x1 = x1 - 20 
            x2 = x2 + 10
        else:
            x1 = x1 + 20
            x2 = x2 - 10
    elif end == 'place':
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
    """ arrowhead """

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

def _tokens(sym):
    """ token values """

    _id = refid + '-tokens'

    value = int(INSTANCE.token_ledger[sym])

    # TODO: draw numbers <= 5 as dots
    if value == 1:

        return PAPER.circle({
            'cx': float(_attr(sym).x2.value),
            'cy': float(_attr(sym).y2.value),
            'r': 2
        }).attr({
            'id': _id,
            'class': 'tokens',
            'fill': '#000',
            'fill-opacity': 1,
            'stroke': '#000',
            'orient': 0 
        })

    if value == 0:
        _txt = ''
    else:
        _txt = str(value)

    return PAPER.text(float(_attr(sym).x2.value), float(_attr(sym).y2.value), _txt)

def _label(sym):
    """ labels """

    _id = refid + '-label'

    _txt = SYMBOLS[sym].data('label')

    el = PAPER.text(float(_attr(sym).x2.value) - 10, float(_attr(sym).y2.value) + 35, _txt)
    el.attr({ 'class': 'label', 'style': 'font-size: 12px;'})
    return el

def _handle(x=0, y=50, size=40, refid=None, symbol=None):
    """ add group of elements needed for UI interaction """
    _id = refid + '-handle'

    point = SYMBOLS[refid]
    handle = PAPER.g(point, _label(refid))

    if symbol == 'place':
       el = _place(x=x, y=y, size=size, refid=refid, symbol=symbol)
       el.data('refid', refid)
       token_el = _tokens(refid)
       INSTANCE.token_ledger[refid]
       handle.add(el, token_el)

    elif symbol == 'transition':
       el = _transition(x=x, y=y, size=size, refid=refid, symbol=symbol)
       handle.add(el)

    el.data('refid', refid)
    SYMBOLS[_id] = handle

    def _drag_start(*args):
        pass

    def _drag_end(mouseevent):

        def _move_and_redraw():
            new_coords = [mouseevent.offsetX, mouseevent.offsetY]
            if symbol == 'place':
                INSTANCE.place_defs[refid]['position'] = new_coords
            elif symbol == 'transition':
                INSTANCE.transition_defs[refid]['position'] = new_coords

            render()

        reset(callback=_move_and_redraw)

    def _dragging(dx, dy, x, y, event):
        _tx = 't %i %i' % (dx, dy)
        handle.transform(_tx)
    
    handle.drag(_dragging, _drag_start, _drag_end)

    return handle

def _transition(x=0, y=50, size=40, refid=None, symbol=None):
    """ draw transition """

    _id = '%s-%s' % (refid, symbol)

    return PAPER.rect({
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

def _place(x=0, y=50, size=40, refid=None, symbol=None):
    """ draw place """

    _id = '%s-%s' % (refid, symbol)

    return PAPER.circle({
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
