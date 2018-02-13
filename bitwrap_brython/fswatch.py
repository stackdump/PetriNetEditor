""" watch for modifications to ./docs folder """

from twisted.internet import inotify
from twisted.python import filepath
from twisted.application.service import IService
from zope.interface import implements
from txbitwrap.event.dispatch import Dispatcher

class FsWatch(object):
    """
    watch ./docs for changes and dispatch an event to message bus
    """

    implements(IService)

    def __init__(self, web_root):
        self.name = __name__
        self.web_root = web_root
        self.notifier = inotify.INotify()

    def privilegedStartService(self):
        """ required by IService """

    def startService(self):
        """ start service """
        print '__SERVICE__ => ' + self.name
        self.notifier.startReading()
        self.notifier.watch(filepath.FilePath(self.web_root), callbacks=[self.fs_changed])

    def stopService(self):
        """ stop service """
        print 'stopping %s' % self.name

    def fs_changed(self, _, path, mask):
        if not str.endswith(filepath.FilePath.basename(path), '.py'):
           return

        fsmask = ', '.join(inotify.humanReadableMask(mask))

        if not 'modify' in fsmask:
           return

        print "event %s on %s" % (', '.join(inotify.humanReadableMask(mask)), path)

        Dispatcher.send({
            'schema': 'brython',
            'oid': 'fswatch',
            'action': fsmask,
            'payload': { 'filepath': str(path) }
        })
