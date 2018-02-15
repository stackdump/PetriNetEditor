""" ctx: Bitwrap 'context' - see command list: ctx.commands - see docstring: help(ctx.<command>) """

import dsl
import json
from browser import window
from dsl import subscribe, unsubscribe, echo # util
from dsl import load, create, destroy # modify stream
from dsl import schemata, state, machine, dispatch, stream, event, exists # use stream

commands = [
    'subscribe',
    'unsubscribe',
    'load',
    'create',
    'destroy',
    'schemata',
    'state',
    'machine',
    'dispatch',
    'stream',
    'event',
    'exists'
]

from dsl import subscribe, unsubscribe, echo # util
from dsl import load, create, destroy # modify stream
from dsl import schemata, state, machine, dispatch, stream, event, exists # use stream

import net

def __onload(req):
    """ init config and connections """
    config = json.loads(req.response)
    dsl.__onload(config)
    net.__onload(dsl)

dsl._get(window.Bitwrap.config, __onload)
