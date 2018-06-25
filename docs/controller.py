import json
from browser import window, console
from importer import Importer

class Controller(object):
    """ control loading and saving network definitions """

    def __init__(self, context=None, editor=None, default_net='counter'):
        self.editor = editor
        self.ctx = context
        self.select_net = default_net
        self.view(select_net=default_net)
        self.ctx.schemata(callback=self.load_saved_nets)
        self.bind_controls()

    def bind_controls(self):
        """ control editor instance """
        window.jQuery('#netreload').on('click', lambda _: self.view())

    def load_saved_nets(self, req):
        """ load known schemata from server """
        nets = Importer.parse_file_list(req.text)['schemata']
        options = []

        for net in nets:
            if self.selected_net == net:
                options.append('<option selected="selected">%s</option>' % net)
            else:
                options.append('<option>%s</option>' % net)

        el = window.jQuery('#netselect')
        el.html(''.join(options))
        el.change(lambda event: self.view(event.target.value))

    def view(self, select_net=None):
        """ open net with editor """
        if select_net:
            self.selected_net = select_net

        self.editor.open(self.selected_net)
