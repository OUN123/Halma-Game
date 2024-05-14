
import copy

class Player:
  def __init__(self, color, boardSize):
    self.color = color
    self.makeRegionpions(boardSize)
    self.homeCoord = []
    self.goalCoord = []
    
  def makeRegionpions(self, boardSize):
    self.pions = []
    self.home = []
    self.goal = []
    if boardSize == 8:
      maxIter = 5
    elif boardSize == 10:
      maxIter = 6
    else: # default is 16 x 16
      maxIter = 7

    for i in range(1, maxIter):
      for j in range(1, maxIter):
        if (i + j <= maxIter and i < maxIter and j < maxIter):
          self.pions.append(Pion(boardSize - j + 1, boardSize - i + 1))
          self.home.append((boardSize - j + 1, boardSize - i + 1))
          self.goal.append((j, i))

    if self.color == 'RED':
      # If an opposing player
      temp = copy.deepcopy(self.home)
      self.home = copy.deepcopy(self.goal)
      self.goal = temp
      for i in range(len(self.pions)):
        self.pions[i].x = self.home[i][0]
        self.pions[i].y = self.home[i][1]
              

  def printStatus(self):
    print('Color: '+ self.color)
    print('Position of pions:')
    for pion in self.pions:
      print('({x}, {y}), IsArrived={IsArrived}, IsDeparted={IsDeparted}'.format(x=pion.x, y=pion.y, IsArrived=pion.IsArrived, IsDeparted=pion.IsDeparted))
  
  #all pion in oponent base
  def isTerminate(self):
    status = True
    for p in self.pions:
        if (p.x, p.y) in self.goal:
            status = True
        else:
            status = False
            break
    return status
  
  #cek if pions contain x and y, true if yes
  def isExist_pions(self,x,y):
    for i in range(len(self.pions)):
      if(self.pions[i].x == x and self.pions[i].y== y ):
        return True
        break
      else:
        pass
    return False
  
  def isExist_home(self,x,y):
    koor =(x, y)
    if koor in self.home:
      return True
    else:
      return False
    
  def isExist_goal(self,x,y):
    koor =(x, y)
    if koor in self.goal:
      return True
    else:
      return False
  
  def getpion(self, row, column):
    i = 0
    found = False
    while i < len(self.pions) and not(found):
      if (self.pions[i].x == row and self.pions[i].y == column):
        pion = self.pions[i]
        return pion
        found = True
      else:
        i +=1

  def tempMovepion(self, from_tile, to_tile):
    (x, y) = from_tile
    (x2, y2) = to_tile
    for p in self.pions:
      if p.x == x and p.y == y:
        p.x = x2
        p.y = y2
        self.pions = sorted(self.pions, key=lambda p: (p.x, p.y))
        break

  def movepion(self, from_tile, to_tile):
    (x, y) = from_tile
    (x2, y2) = to_tile
    for p in self.pions:
      if p.x == x and p.y == y:
        if (x, y) in self.home and (x2, y2) not in self.home:
          p.IsDeparted = True
        elif (x, y) not in self.goal and (x2, y2) in self.goal:
          p.IsArrived = True
        p.x = x2
        p.y = y2
        self.pions = sorted(self.pions, key=lambda p: (p.x, p.y))
        break

class Pion:
  def __init__(self, x, y):
    self.setCoordinate(x, y)
    self.setIsDeparted(False)
    self.setIsArrived(False)

  def setCoordinate(self,x, y):
    self.x = x
    self.y = y

  def setIsDeparted(self, IsDeparted):
    self.IsDeparted = IsDeparted
    
  def setIsArrived(self, IsArrived):
    self.IsArrived = IsArrived
  
  def getCoordinateX(self):
    return (self.x)
  
  def getCoordinateY(self):
    return (self.y)
  
  def getCoordinate(self):
    return (self.x, self.y)  