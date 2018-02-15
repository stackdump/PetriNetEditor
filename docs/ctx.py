""" ctx: Bitwrap 'context' - see command list: ctx.commands - see docstring: help(ctx.<command>) """

import dsl
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

def __onload():
    """ init config and connections """
    dsl._get(window.Bitwrap.config, dsl.__onload)
    net.__onload(dsl)

__onload()
