# Used for delaying each loop
from time import sleep
# Used for holding the players
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
import random

class ClientChannel(Channel):
    #This is the server representation of a single connected client.
    def __init__(self, *args, **kwargs):
        self.nickname = "Anonymous"
        Channel.__init__(self, *args, **kwargs)
    
    def Close(self):
        self._server.DelPlayer(self)

    def Network_disconnect(self, data):
        self.Close()
    #### My code start ####
    def getPlayer(self, stri):
        # This function will return the player associated with that name
        for p in self._server.players:
            if p.nickname == stri:
                return p
    def Network_loc(self, data):
        # Called when a player changes direction
        # data contains the location, and the direction of the player who sent it
        for p in self._server.players:
            if p != self:
                self._server.SendToPlayer(p, {"action":"loc", "loc":data['loc'], "dir":data['dir']})
    def Network_food(self, data):
        # This is called when a player eats a food
        for p in self._server.players:
            if p != self:
                # Since the client determines the new food location,
                # we just send the other player the new location, and which food it is (1 or 2)
                self._server.SendToPlayer(p, {"action":"food", "which":data['which'], "new":data['new']})    
    def Network_death(self, data):
        # This is called when a player dies.
        # Then we send to the other player that they died
        for p in self._server.players:
            # This makes it so its only sent to the other player
            if p != self:
                self._server.SendToPlayer(p, {"action":"death"})
    #### My code end ####
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
        # Check if the player count is 2
        if len(self.players) == 2:
            i = 1
            # If so, send the players their starting positions
            for p in self.players:
                # We tell them their position and food start positions
                x = random.randint(50, 590)
                y = random.randint(50, 350)
                x2 = random.randint(50, 590)
                y2 = random.randint(50, 350)
                height = random.randint(10,21)
                height2 = random.randint(10,21)
                p.Send({"action":"ready", "pos":i, 'food1':(x,y, height),'food2':(x2,y2, height2)})
                i += 1
        sleep(1)
    
    def DelPlayer(self, player):
        # Called when a player quits
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

# Assign the server to localhost, with the port 12345
s = ChatServer(localaddr=("localhost", 12345))
# Launch the server
s.Launch()