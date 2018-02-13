import os
from zope.interface import implements
from twisted.application import service, internet
from twisted.application.service import IServiceMaker, MultiService
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.plugin import IPlugin
from txbitwrap.event.dispatch import Dispatcher
from txbitwrap.event import rdq
from txbitwrap import Options
from bitwrap_brython.fswatch import FsWatch
from bitwrap_brython.api import factory as ApiFactory
Factory.noisy = False

class ServiceFactory(object):
    implements(IServiceMaker, IPlugin)

    tapname = "brython"
    description = "bitwrap eventstore with a brython frontend"
    options = Options

    def makeService(self, options):
        multi_service = MultiService()
        Options.append_env(options)

        options['template_path'] = os.path.abspath(os.path.dirname(__file__) + '/../../templates')

        bitwrap_node = internet.TCPServer(
            int(options['listen-port']),
            ApiFactory(options),
            interface=options['listen-ip']
        )

        htdocs = os.path.abspath(os.path.dirname(__file__) + '/../../docs')
        multi_service.addService(FsWatch(htdocs))

        multi_service.addService(bitwrap_node)
        multi_service.addService(Dispatcher(rdq, options))


        return multi_service

serviceMaker = ServiceFactory()
