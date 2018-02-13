from txbitwrap.api import *
from cyclone.web import StaticFileHandler

VERSION='20180128'

class BrythonConfig(headers.Mixin, RequestHandler):
    """ config """

    def get(self, stage, *args):
        """ direct web app to api """

        self.write({
            'endpoint': os.environ.get('ENDPOINT', 'http://' + self.request.host),
            'version': VERSION,
            'stage': stage,
            'use_websocket': True
        })

class BrythonIndex(RequestHandler):
    """ index """

    def get(self):
        self.render(
            "index.html",
            app_root=os.environ.get('APP_ROOT', ''),
        )


def factory(options):
    """ cyclone app factory """

    handlers = [
        (r"/dispatch/(.*)/(.*)/(.*)", Dispatch),
        (r"/broadcast/(.*)/(.*)", Broadcast),
        (r"/websocket", WebSocketBroker),
        (r"/event/(.*)/(.*)", Event),
        (r"/state/(.*)/(.*)", State),
        (r"/machine/(.*)", Machine),
        (r"/schemata", Schemata),
        (r"/stream/(.*)/(.*)", Stream),
        (r"/config/(.*).json", BrythonConfig),
        (r"/api", rpc.Rpc),
        (r"/", BrythonIndex),
        (r"/(.*\.py)", StaticFileHandler, {"path": "./docs"})
    ]

    return cyclone.web.Application(handlers, **settings(options))
