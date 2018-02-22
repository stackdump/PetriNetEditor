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
        CTL.reset(callback=CTL.render)

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
            net.PNet(CTL)

        net.INSTANCE.render()

class Editor(Controller):

    def __init__(self):
        self.callback = self.on_select
        self.move_enabled = True
        self.simulation = None

    def drag_start(self, event):
        """ handle mouse events """
        self.callback(event)
        # TODO: use self.selected

    def on_select(self, event):
        """ callback to show attributes for selected element """
        refid, symbol = str(event.target.id).split('-')
        console.log(refid, symbol)

    def select(self, event):
        self.move_enabled = True
        self.callback = self.on_select

    def symbol(self, event):
        # TODO: should add new symbol
        # this may not need on_symbol callback
        # perhaps add and then go back to select 
        self.callback = self.on_select

    def tool(self, event):
        """ modify existing symbol on net """
        # TODO: find in SYMBOL table and modify properties
        console.log(event.target.text)

    def simulator(self, event):
        """ control start/stop simulation mode """
        self.move_enabled = False
        self.simulation = sim.Simulation(net.INSTANCE, self)
        self.callback = self.simulation.trigger
        console.log(event.target.text)
