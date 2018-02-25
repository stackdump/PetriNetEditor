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

    window.jQuery('#net').on('click', CTL.on_insert)
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

    def select(self, event):
        """ enter select/move mode """
        self.move_enabled = True
        self.selected_insert_symbol = None
        self.callback = self.on_select

    def symbol(self, event):
        """ enter insert symbol mode """
        sym = str(event.target.id)
        self.selected_insert_symbol = sym

    def on_insert(self, event):
        """ insert a symbol into net """
        if not self.selected_insert_symbol:
            return

        new_coords = [event.offsetX, event.offsetY]
        # TODO: make call to insert new symbol in INSTANCE

        if self.selected_insert_symbol == 'place':
            net.INSTANCE.insert_place(new_coords)
        else:
            net.INSTANCE.insert_transition(new_coords)

        self.reset(callback=self.render)

    def simulator(self, event):
        """ control start/stop simulation mode """
        target_id = event.target.text

        if target_id == 'reset':
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
        self.move_enabled = False
        self.selected_insert_symbol = None
        target_id = str(event.target.id)

        if target_id == 'arc':
            # TODO: should put into mode where we select input arc
            console.log('start arc creation') # next selected handle is 'start' 
        elif target_id == 'delete':
            self.callback = self.on_delete

    def on_delete(self, event):
        """ callback when clicking elements when delete tool is active """
        target_id = str(event.target.id)

        if not self.is_selectable(target_id):
            return

        refid, symbol = target_id.split('-')

        if symbol == 'place':
            net.INSTANCE.delete_place(refid)
        elif symbol == 'transition':
            net.INSTANCE.delete_transition(refid)
        else:
            net.INSTANCE.delete_arc(target_id)

        self.reset(callback=self.render)
