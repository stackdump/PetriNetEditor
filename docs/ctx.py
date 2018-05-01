""" ctx: Bitwrap 'context' - see command list: ctx.commands - see docstring: help(ctx.<command>) """

import dsl
import json
from browser import window
from dsl import machine, echo

commands = [ 'machine']

import ctl

def __onload(req):
    """ init config and connections """
    config = json.loads(req.response)
    dsl.__onload(config)
    ctl.__onload(dsl)

dsl._get(window.Bitwrap.config, __onload)
