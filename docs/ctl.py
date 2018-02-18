from browser import window, document, console
import net
import json


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
    net.SCHEMA = pnet['machine']['name']
    net.NETS[net.SCHEMA] = pnet['machine']
    reset(callback=render)

def reset(callback=None):
    """ clear SVG and prepare markers """
    net.PAPER
    
    if not net.PAPER:
        net.PAPER=window.Snap('#net')

    net.PAPER.clear()
    net._load_symbols()
    net._origin()

    if callback:
        callback()

def render():
    """ development examples """
    if not net.INSTANCE:
        net.INSTANCE = net.PNet()

    net.INSTANCE.render()
