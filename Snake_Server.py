from time import sleep
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
    #This is the server representation of a single connected client.
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    ##################################
    ### Network specific callbacks ###
    ##################################
    def getPlayer(self, stri):
        for p in self._server.players:
            if p.nickname == stri:
                return p
    def Network_disconnect(self, data):
        self.Close()
    def Network_loc(self, data):
        print data
        for p in self._server.players:
            if p != self:
                self._server.SendToPlayer(p, {"action":"loc", "loc":data['loc'], "dir":data['dir']})
    def Network_food(self, data):
        print data
        for p in self._server.players:
            if p != self:
                self._server.SendToPlayer(p, {"action":"food", "which":data['which'], "new":data['new']})    
    def Network_death(self, data):
        print data
        for p in self._server.players:
            if p != self:
                self._server.SendToPlayer(p, {"action":"death"})
    def Network_nickname(self, data):
        self.nickname = data['nickname']
        self._server.SendPlayers()
class ChatServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print 'Server launched'
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
    
    def AddPlayer(self, player):
        print "New Client: "+str(player.addr)
        self.players[player] = True
        self.SendPlayers()
        if len(self.players) == 2:
            x = 1
            for p in self.players:
                p.Send({"action":"ready", "pos":x, 'food1':(50,234, 15),'food2':(200,320, 11)})
                x += 1
        sleep(1)
    
    def DelPlayer(self, player):
        print "Deleting Client: " +str(player.addr)
        del self.players[player]
        self.SendPlayers()
    
    def SendPlayers(self):
        nicks = []
        for p in self.players:
            nicks.append(p.nickname)
        self.SendToAll({"action": "players", "players": nicks})
    
    def SendToPlayer(self, player, data):
        player.Send(data)
    
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
s = ChatServer(localaddr=("localhost", 12345))

s.Launch()
