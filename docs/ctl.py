from browser import window, document, console
import net
import sim
import json

CTX = None
"""
Bitwrap context
"""

CTL = None
"""
UI control interface
"""

def __onload(ctx):
    """ use snap to begin creating an SVG """
    global CTL
    CTL = Editor()

    window.jQuery('#net').on('click', CTL.insert)
    window.jQuery('.select').on('click', CTL.select)
    window.jQuery('.symbol').on('click', CTL.symbol)
    window.jQuery('.tool').on('click', CTL.tool)
    window.jQuery('.simulator').on('click', CTL.simulator)

    global CTX
    CTX = ctx
    CTX.machine('octoe', callback=CTL.load)

class Controller(object):
    """ Provide interface for UI actions """

    def load(self, res):
        """ store requested PNML and render as SVG """
        pnet = json.loads(res.text)
        net.SCHEMA = pnet['machine']['name']
        net.NETS[net.SCHEMA] = pnet['machine']
        self.reset(callback=self.render)

    def reset(self, callback=None):
        """ clear SVG and prepare markers """
        net.PAPER
        
        if not net.PAPER:
            net.PAPER=window.Snap('#net')

        net.PAPER.clear()
        net._load_symbols()
        net._origin()

        if callback:
            callback()

    def render(self):
        """ development examples """
        if not net.INSTANCE:
            net.PNet(self)

        net.INSTANCE.render()

class Editor(Controller):

    def __init__(self):
        self.callback = self.on_select
        self.move_enabled = True
        self.selected_insert_symbol = None
        self.simulation = None

    def is_selectable(self, target_id):
        console.log(target_id)

        if '-' not in target_id:
            return False
        else:
            return True

    def drag_start(self, event):
        """ handle mouse events """
        self.callback(event)

    def on_select(self, event):
        """ callback to show attributes for selected element """
        target_id = str(event.target.id)

        if not self.is_selectable(target_id):
            return

        refid, symbol = target_id.split('-')
        console.log(refid, symbol)

    def select(self, event):
        """ enter select/move mode """
        self.move_enabled = True
        self.selected_insert_symbol = None
        self.callback = self.on_select

    def symbol(self, event):
        """ enter insert symbol mode """
        sym = str(event.target.id)
        self.selected_insert_symbol = sym

    def insert(self, event):
        """ insert a symbol into net """
        if not self.selected_insert_symbol:
            return

        new_coords = [event.offsetX, event.offsetY]
        # TODO: make call to insert new symbol in INSTANCE

        if self.selected_insert_symbol == 'place':
            self._insert_place(new_coords)
        else:
            self._insert_transition(new_coords)

        self.reset(self.render)

    def _insert_place(self, coords, inital=0):
        _offset = net.INSTANCE.vector_size
        net.INSTANCE.vector_size = _offset + 1

        label = 'p%i' % _offset

        console.log(coords, 'insert-place', label)

        net.INSTANCE.place_defs[label] = {
            'position': coords,
            'inital': inital,
            'offset': _offset
        }

        net.INSTANCE.token_ledger[label] = inital

        for name, attr in net.INSTANCE.transition_defs.items():
            attr['delta'].append(0)

    def _insert_transition(self, coords):
        size = len(net.INSTANCE.transition_defs)

        label = 't%i' % size

        console.log(coords, 'insert-transition', label)

        net.INSTANCE.transition_defs[label] = {
            'position': coords,
            'role': 'default',
            'delta': [0] * net.INSTANCE.vector_size
        }

    def simulator(self, event):
        """ control start/stop simulation mode """
        target_id = event.target.text
        console.log(target_id)

        if target_id == 'reset':
            console.log('reset simulation')
            if self.simulation:
                self.simulation.reset()
            self.callback = self.on_select
            self.move_enabled = True
        else:
            self.move_enabled = False
            self.simulation = sim.Simulation(net.INSTANCE, self)
            self.callback = self.simulation.trigger

    def tool(self, event):
        """ modify existing symbol on net """
        target_id = str(event.target.id)

        if target_id == 'arc':
            # TODO: should put into mode where we select input arc
            self.move_enabled = False
            console.log('start arc creation') # next selected handle is 'start' 
        elif target_id == 'delete':
            self.callback = self.on_delete

    def on_delete(self, event):
        """ callback when clicking elements when delete tool is active """
        target_id = str(event.target.id)

        console.log(target_id)
        if not self.is_selectable(target_id):
            return

        refid, symbol = target_id.split('-')

        if symbol == 'place':
            self._delete_place(refid)
        elif symbol == 'transition':
            self._delete_transition(refid)
        else:
            self._delete_arc(target_id)
            

    def _delete_place(self, refid):
        console.log('delete place', refid)

    def _delete_transition(self, refid):
        console.log('delete place', refid)

    def _delete_arc(self, refid):
        console.log('delete arc', refid)

