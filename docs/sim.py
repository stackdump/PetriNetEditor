class Simulation(object):
    """ use pnet to run a simulation """

    def __init__(self, net, control):
        self.pnet = net
        self.ctl = control
        self.history = []

    def trigger(self, event):
        """ callback to trigger live transition during simulation """
        refid, symbol = str(event.target.id).split('-')

        if not self.pnet or not symbol == 'transition':
            return

        if self.pnet.commit(refid):
            self.history.append(refid)
            console.log(refid)
            self.ctl.reset(callback=self.ctl.render)

    def hilight_live_transitions(self):
        pass

