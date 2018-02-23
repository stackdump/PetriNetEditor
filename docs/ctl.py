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
        pnet  = json.loads(res.text)
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
        console.log(event, 'insert-' + self.selected_insert_symbol)

    def simulator(self, event):
        """ control start/stop simulation mode """
        self.move_enabled = False
        self.simulation = sim.Simulation(net.INSTANCE, self)
        self.callback = self.simulation.trigger
        console.log(event.target.text)

    def tool(self, event):
        """ modify existing symbol on net """
        target_id = str(event.target.id)

        if target_id == 'arc':
            # TODO: should put into mode where we select input arc
            self.move_enabled = False
            console.log('start arc creation') # next selected handle is 'start' 

        # TODO: should allow another tool mode that
        # allows element attributes to be edited from the UI
