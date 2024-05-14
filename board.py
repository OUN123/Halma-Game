from player import Player, Pion
from coordinate import Coordinate
import math
import time
import copy

class Board:
  def __init__(self, boardSize, timeLimit, p1, p2, selfplay, bot):
    self.boardSize = boardSize
    self.timelimit = timeLimit
    self.player1 = p1
    self.player2 = p2
    self.g_player = p1 if p1.color == "GREEN" else p2
    self.r_player = p2 if p2.color == "RED" else p1
    self.turn = 1
    self.coordinate = [[Coordinate(i, j) for i in range(self.boardSize)] for j in range(self.boardSize)]
    self.depth = 2
    self.selfplay = selfplay
    self.bot = bot
    
    if self.boardSize == 8:
      maxIter = 4
    elif self.boardSize == 10:
      maxIter = 5
    else: # default is 16 x 16
      maxIter = 6

    for i in range(maxIter):
      for j in range(maxIter):
        if (i + j < maxIter and i < 6 and j < 6):
          self.coordinate[i][j].color = "RED"
          self.coordinate[i][j].pion = 2
          self.r_player.homeCoord.append(self.coordinate[i][j])
          self.g_player.goalCoord.append(self.coordinate[i][j])
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].color = "GREEN"
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].pion = 1
          self.g_player.goalCoord.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])
          self.r_player.homeCoord.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])

  def printBoard(self):
    for i in range(self.boardSize + 1):
      if (i == 0):
        print("    ", end="")
        for j in range(self.boardSize):
          if j < self.boardSize - 1:
            print(chr(j+97) + " ", end="")
          else:
            print(chr(j+97) + " ")
      else:
        num = str(i) + "   " if i < 10 else str(i) + "  "
        print(num, end="")
        for j in range(self.boardSize):
          if j < self.boardSize - 1:
            if (self.coordinate[i-1][j].pion == 1):
              print("G ", end="")
            elif (self.coordinate[i-1][j].pion == 2):
              print("R ", end="")
            else:
              print("* ", end="")
          else:
            if (self.coordinate[i-1][j].pion == 1):
              print("G ")
            elif (self.coordinate[i-1][j].pion == 2):
              print("R ")
            else:
              print("* ")
  
  def getSize(self):
    return self.boardSize
  
  def isEmpty(self,x,y):
    if(self.player1.isExist_pions(x,y) or self.player2.isExist_pions(x,y)):
      return False
    else:
      return True
  
  def isKoordHome(self, player, x, y):
    return(player.isExist_home(x,y))
      
  def isKoordGoal(self, player, x, y):
    return(player.isExist_goal(x,y)) 
    
  def checkAvailablePosition(self, position, delta):
    x, y = position
    availablePosition = []

    if (delta == 1):
      availablePosition.append((x+1, y))
      availablePosition.append((x+1, y+1))
      availablePosition.append((x, y+1))
      availablePosition.append((x-1, y+1))
      availablePosition.append((x-1, y))
      availablePosition.append((x-1, y-1))
      availablePosition.append((x, y-1))
      availablePosition.append((x+1, y-1))
    else:
      if (not(self.isEmpty(x+1,y)) and (self.isEmpty(x+2, y))):
        availablePosition.append((x+2, y))
      if (not(self.isEmpty(x-1,y)) and (self.isEmpty(x-2, y))):
        availablePosition.append((x-2, y))
      if (not(self.isEmpty(x,y+1)) and (self.isEmpty(x, y+2))):
        availablePosition.append((x, y+2))
      if (not(self.isEmpty(x,y-1)) and (self.isEmpty(x, y-2))):
        availablePosition.append((x, y-2))
      if (not(self.isEmpty(x+1,y+1)) and (self.isEmpty(x+2, y+2))):
        availablePosition.append((x+2, y+2))
      if (not(self.isEmpty(x+1,y-1)) and (self.isEmpty(x+2, y-2))):
        availablePosition.append((x+2, y-2))
      if (not(self.isEmpty(x-1,y+1)) and (self.isEmpty(x-2, y+2))):
        availablePosition.append((x-2, y+2))
      if (not(self.isEmpty(x-1,y-1)) and (self.isEmpty(x-2, y-2))):
        availablePosition.append((x-2, y-2))
    
    length = len(availablePosition)
    i = 0
    while (i < length):
      (x, y) = availablePosition[i]
      # if outside the board
      if(x<1 or y<1 or x>self.boardSize or y>self.boardSize):
        availablePosition.remove(availablePosition[i])
        length -= 1

      # if there is content
      elif (delta == 1 and not(self.isEmpty(x, y))):
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1
    return availablePosition

  def getJump(self, position, jumps, last_position):
    availableJumps = self.checkAvailablePosition(position, 2)

    try:
      availableJumps.remove(last_position)
    except:
      pass

    if (len(availableJumps) ==  0):
      return jumps
    else:
      for i in range (len(availableJumps)):
        if availableJumps[i] not in jumps:
          jumps.append(availableJumps[i])
          self.getJump(availableJumps[i], jumps, position)
        
  def getAksiValid(self, pion):
    if (self.player1.isExist_pions(pion.x, pion.y)):
        player = self.player1
    else:
        player = self.player2

    # Current position
    current_position = (pion.x, pion.y)

    # available positions
    availablePosition = self.checkAvailablePosition(current_position, 1)
    availableJump = self.checkAvailablePosition(current_position, 2)

    if (len(availableJump) > 0):
      for i in range (len(availableJump)):
        if (availableJump[i] not in availablePosition):
          availablePosition.append(availableJump[i])
        jumps = []
        self.getJump(availableJump[i], jumps, current_position)
        if (len(jumps) > 0):
          for i in range (len(jumps)):
            if (jumps[i] not in availablePosition):
              availablePosition.append(jumps[i])
    
    # Check out home or incoming base
    length = len(availablePosition)
    i = 0
    while (i < length):
      (x, y) = availablePosition[i]
      if (pion.IsArrived and not(self.isKoordGoal(player, x, y))) or (pion.IsDeparted and (self.isKoordHome(player, x ,y))):
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1
    availablePosition = sorted(availablePosition, key=lambda tup: (tup[0], tup[1]))
    return availablePosition

  def objectiveFunc(self, player):
    def point_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def defensive_positioning(x, y, player):
        # Simplistic example: Check adjacent tiles for own pawns
        count = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.boardSize and 0 <= ny < self.boardSize and self.coordinate[ny][nx].pion == self.coordinate[y][x].pion:
                count += 1
        return count

    def path_clearance(x, y, player):
        # Count clear paths to the goal
        clear_paths = 0
        for gx, gy in player.goal:
            if self.coordinate[gy-1][gx-1].pion == 0:
                clear_paths += 1
        return clear_paths

    val = 0
    for x in range(self.boardSize):
        for y in range(self.boardSize):
            c = self.coordinate[y][x]
            if (player.color == "GREEN" and c.pion == 1) or (player.color == "RED" and c.pion == 2):
                goalDistance = [point_distance(c.x, c.y, gx-1, gy-1) for gx, gy in player.goal if self.coordinate[gy-1][gx-1].pion != c.pion]
                defensive_score = defensive_positioning(c.x, c.y, player)
                path_score = path_clearance(c.x, c.y, player)

                # Calculate the weighted value of each strategy
                distance_val = max(goalDistance) if goalDistance else -50
                val += (0.7 * distance_val) + (0.2 * defensive_score) + (0.1 * path_score)

    val *= -1  # Convert to a more standard min-max format where higher is better
    return val


  def minimax(self, depth, playermax, playermin, timelimit, isLocalSearch, a=float("-inf"), b=float("inf"), isMax=True):
    # basis
    if depth == 0 or time.time() > timelimit:
      return self.objectiveFunc(playermax), None

    bestmove = None
    if isMax:
      bestval = float("-inf")
      if isLocalSearch:
        possiblemoves = self.localSearch(playermax)
      else:
        possiblemoves = self.getPlayerMoves(playermax)
        
    else:
      bestval = float("inf")
      if isLocalSearch:
        possiblemoves = self.localSearch(playermin)
      else:
        possiblemoves = self.getPlayerMoves(playermin)

     # for every possible move
    for move in possiblemoves:
      for to in move["to"]:
        # Exit when exceeding timelimit
        if time.time() > timelimit:
          return bestval, bestmove

        # temporarily move pawns
        self.tempMovepion((move["from"].y+1, move["from"].x+1), (to.y+1, to.x+1))

        # Minimax Recursive
        val, _ = self.minimax(depth - 1, playermax, playermin, timelimit, isLocalSearch, a, b, not isMax)

         # Return the pawn to its original place
        self.tempMovepion((to.y+1, to.x+1), (move["from"].y+1, move["from"].x+1))

        if isMax and val > bestval:
          bestval = val
          bestmove = ((move["from"].y+1, move["from"].x+1), (to.y+1, to.x+1))
          a = max(a, val)

        if not isMax and val < bestval:
          bestval = val
          bestmove = ((move["from"].y+1, move["from"].x+1), (to.y+1, to.x+1))
          b = min(b, val)

        # alpha beta pruning
        if b <= a:
          return bestval, bestmove

    return bestval, bestmove

 # localsearch reduces the number of moves that can be taken from a pawn
  # by taking the goal step that has the greatest obj function value
  def localSearch(self, player):
    possiblemoves = []
    for p in player.pions:
      moves = []
      validactions = self.getAksiValid(p)
      if (len(validactions) == 0):
        continue
      else:
        temp = copy.deepcopy(p)
        (x, y) = validactions[0]
        validactions.remove((x, y))

        self.tempMovepion((p.y, p.x), (y, x))
        bestval = self.objectiveFunc(player)
        self.tempMovepion((y, x), (temp.y, temp.x))
        moves.append((x, y))
        
        for va in validactions:
          self.tempMovepion((p.y, p.x), (va[1], va[0]))
          val = self.objectiveFunc(player)
          self.tempMovepion((va[1], va[0]), (temp.y, temp.x))

          # player maximum
          if ((player.color == self.player1.color and self.turn == 1) or (player.color == self.player2.color and self.turn == 2)):
            if (val > bestval or (va[0], va[1]) in player.goal):
              moves.clear()
              moves.append((va[0], va[1]))
              bestval = val
            elif (val == bestval or (va[0], va[1]) in player.goal):
              moves.append((va[0], va[1]))
          #player minimum
          else:
            if (val < bestval):
              moves.clear()
              moves.append((va[0], va[1]))
              bestval = val
            elif (val == bestval):
              moves.append((va[0], va[1]))
        
        curr_tile = self.coordinate[p.y-1][p.x-1]
        move = {
          "from": curr_tile,
          "to": self.getMovesCoord(moves)
        }
        possiblemoves.append(move)
    
    return possiblemoves
          
  def getPlayerMoves(self, player):
    moves = []  # All possible moves
    for p in player.pions:
      curr_tile = self.coordinate[p.y-1][p.x-1]
      move = {
        "from": curr_tile,
        "to": self.getMovesCoord(self.getAksiValid(p))
      }
      moves.append(move)
    return moves

  def getMovesCoord(self, validactions):
    moves = []
    for l in validactions:
      el = self.coordinate[l[1]-1][l[0]-1]
      moves.append(el)
    return moves

  def movepion(self, from_coord, to_coord):
    from_tile = self.coordinate[from_coord[0]-1][from_coord[1]-1]
    to_tile = self.coordinate[to_coord[0]-1][to_coord[1]-1]
    
    # if you move from an empty tile or move to a tile with pawns
    if from_tile.pion == 0 or to_tile.pion != 0:
      print("Invalid move pion!")
      return

     # Move pawn
    if from_tile.pion == 1:
      self.g_player.movepion((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    elif from_tile.pion == 2:
      self.r_player.movepion((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    else:
      print("Invalid move pion!")
      return
    to_tile.pion = from_tile.pion
    from_tile.pion = 0

  def tempMovepion(self, from_coord, to_coord):
    from_tile = self.coordinate[from_coord[0]-1][from_coord[1]-1]
    to_tile = self.coordinate[to_coord[0]-1][to_coord[1]-1]
    
    # temporarily move pawns
    if from_tile.pion == 1:
      self.g_player.tempMovepion((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    elif from_tile.pion == 2:
      self.r_player.tempMovepion((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    else:
      print("invalid temp move pion")
      return
    to_tile.pion = from_tile.pion
    from_tile.pion = 0

  def executeBotMove(self):
    max_time = time.time() + self.timelimit

    # call minimax search function
    if (self.selfplay):
      playermax = self.player1 if self.turn == 1 else self.player2
      playermin = self.player2 if self.turn == 1 else self.player1
      if (self.turn == 2):
        _, move = self.minimax(self.depth, playermax, playermin, max_time, True)
      else:
        _, move = self.minimax(self.depth, playermax, playermin, max_time, False)
    else:
      playermax = self.player2
      playermin = self.player1
      if (self.bot == "MLS"):
        _, move = self.minimax(self.depth, playermax, playermin, max_time, True)
      else:
        _, move = self.minimax(self.depth, playermax, playermin, max_time, False)

   # Move pawn
    if move is None:
      print("Status: no action taken")
    else:
      (x1, y1) = move[0]
      (x2, y2) = move[1]
      self.movepion((x1, y1), (x2, y2))
      print("Status: pion", (y1, x1), "moved to", (y2, x2))

  def getMoveFromTile(self, player, x, y):
    p = player.getpion(x, y)
    return self.getAksiValid(p) 