from browser import window, document, console
import net
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

    def dispatch(self, event):
        """ handle mouse events """
        self.callback(event)
        # TODO: use self.selected

    def on_select(self, event):
        """ callback to show attributes for selected element """
        refid, symbol = str(event.target.id).split('-')
        console.log(refid, symbol)

    def select(self, event):
        self.callback = self.on_select

    def symbol(self, event):
        # TODO: should add new symbol
        # this may not need on_symbol callback
        # perhaps add and then go back to select 
        self.callback = self.on_select

    def tool(self, event):
        """ modify existing symbol on net """
        # TODO: find in SYMBOL table and modify
        console.log(event.target.text)

    def on_trigger(self, event):
        """ callback to trigger live transition during simulation """
        refid, symbol = str(event.target.id).split('-')

        if not symbol == 'transition':
            return

        # TODO: change token balance and update state machine
        # REVIEW: where should state vector live?

        console.log(net.SYMBOLS[refid])

    def simulator(self, event):
        """ control start/stop simulation mode """
        # hilight all live transitions
        # selecting a live transition should change token balance
        # and then re-render to hilight live transitions again
        console.log(event.target.text)
        self.callback = self.on_trigger

