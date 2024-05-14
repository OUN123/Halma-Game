class Coordinate:
    def __init__(self, x, y, color="BLACK", pion=0):
        self.x = x
        self.y = y
        self.color = color
        self.pion = pion
        
    def setColor(self, color):
        self.color = color

    def setpion(self, pion):
        self.pion = pion

    def printCoordinate(self):
        print(str(self.x) + str(self.y) + self.color + str(self.pion)) 