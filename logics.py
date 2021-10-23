GRID=[chr(i%8+97)+str(8-i//8) for i in range(64)]
grid=['' for i in range(64)]

def transform_movement(mov:str)->tuple:
  posD=GRID.index(mov[:2])
  if 'x' in mov:
    posA=GRID.index(mov[4:])
  else:
    posA=GRID.index(mov[3:])
  return posD,posA

def isPossibleKnight(posD:int,posA:int,eat:bool)->bool:
  if (abs(posD//8-posA//8),abs(posD%8-posA%8)) in [(2,1),(1,2)]:
    return True
  return False

def isPossibleRook(posD:int,posA:int,eat:bool)->bool:
  if posD%8==posA%8 or posD//8==posA//8:
    return True
  return False

def isPossibleBishop(posD:int,posA:int,eat:bool)->bool:
  if abs(posD//8-posA//8)==abs(posD%8-posA%8):
    return True
  return False

def isPossibleKing(posD:int,posA:int,eat:bool)->bool:
  if (abs(posD//8-posA//8),abs(posD%8-posA%8)) in [(0,1),(1,0),(1,1)]:
    return True
  return False

def isPossiblePawn(posD:int,posA:int,eat:bool,strColor:str)->bool:
  if strColor=='w':
    if posD//8-posA//8==1 and posD%8==posA%8 and not eat:
      return True
    elif posD//8==6 and posD//8-posA//8==2 and not eat:
      return True
    elif abs(posD%8-posA%8)==1 and posD//8-posA//8==1 and eat:
      return True
  else:
    if posA//8-posD//8==1 and not eat:
      return True
    elif posD//8==1 and posA//8-posD//8==2 and not eat:
      return True
    elif abs(posD%8-posA%8)==1 and posA//8-posD//8==1 and eat:
      return True
  return False

def isPossible(mov:str)->bool:
  posD,posA=transform_movement(mov)
  eat='x' in mov
  piece,strColor=grid[posD][1],grid[posD][0]
  if piece=='N':
    return isPossibleKnight(posD,posA,eat)
  elif piece=='R':
    return isPossibleRook(posD,posA,eat)
  elif piece=='B':
    return isPossibleBishop(posD,posA,eat)
  elif piece=='Q':
    return isPossibleRook(posD,posA,eat) or isPossibleBishop(posD,posA,eat)
  elif piece=='K':
    return isPossibleKing(posD,posA,eat)
  elif piece=='p':
    return isPossiblePawn(posD,posA,eat,strColor)

def noInterference(mov:str)->bool:
  posD,posA=transform_movement(mov)
  eat='x' in mov
  strColor=grid[posD][0]
  if len(grid[posA])>0 and strColor == grid[posA][0]:
    return False
  if abs(posA//8-posD//8)<=1 and abs(posA%8-posD%8)<=1:
    return True
  if isPossibleRook(posD,posA,eat):
    #Movement is of type tower movement
    if posA%8==posD%8:
      for i in range(1,abs(posA//8-posD//8)):
        if grid[posD+8*i-16*i*(posA//8<posD//8)]!='':
          return False
      return True
    else:
      for i in range(1,abs(posA%8-posD%8)):
        if grid[posD+i-2*i*(posA%8<posD%8)]!='':
          return False
      return True
  elif isPossibleBishop(posD,posA,eat):
    #Movement is of type bishop movement
    oX=(posA%8>posD%8)
    oY=(posA>posD)
    for i in range(1,abs(posD//8-posA//8)):
      if grid[posD+i*oX+i*8*oY]!='':
        return False
    return True
  else:
    return True

def kingAlreadyInCheck(strColor:str,grid:list)->bool:
  opposite=[]
  allies=[]
  if strColor=='w':
    for i in range(len(grid)):
      if 'b' in grid[i]:
        opposite.append(i)
      elif 'w' in grid[i]:
        allies.append(i)
  else:
    for i in range(len(grid)):
      if 'w' in grid[i]:
        opposite.append(i)
      elif 'b' in grid[i]:
        allies.append(i)
  for pos in opposite:
    mov=GRID[pos]+' x'+GRID[grid.index(strColor+'K')]
    if isPossible(mov) and noInterference(mov):
      return True
  return False

def protectsKing(mov:str)->bool:
  #Simulate situation when piece will have moved and see if king is still in check
  tempGrid=[p for p in grid]#create a temporary grid
  #Move the piece to its new place
  posD,posA=transform_movement(mov)
  strColor=grid[posD][0]
  tempGrid[posA]=tempGrid[posD]
  tempGrid[posD]=''
  #Test if king in check and return contrary value
  return not kingAlreadyInCheck(strColor,tempGrid)
  

def putsKingInCheck(mov:str)->bool:
  posD,posA=transform_movement(mov)
  piece,strColor=grid[posD][1],grid[posD][0]
  if strColor=='w':
    oppColor='b'
  else:
    oppColor='w'
  posK=grid.index(strColor+"K")
  if piece=="K":
    #check that the king does not check himself
    opposite=[i for i in range(63) if len(grid[i])!=0 and grid[i][0]==oppColor]
    putsInCkeck=[i for i in opposite if isPossible(GRID[i]+' x'+GRID[posA]) and noInterference(GRID[i]+' x'+GRID[posA])]
    if len(putsInCkeck)!=0:
      return True
    return False
  elif posD//8==posK//8:
    o=(posD%8>posK%8) - (posD%8<posK%8)
    i=posD%8+o
    while i<8 and i >-1:
      if grid[posD//8*8+i]!='':
        return isPossible(GRID[posD//8*8+i]+" x"+GRID[posK])
      else:
        i+=o
    return False
  elif posD%8==posK%8:
    o=(posD//8>posK//8) - (posD//8<posK//8)
    i=posD//8+o
    while i<8 and i >-1:
      if grid[posD%8+i*8]!='':
        return isPossible(GRID[posD%8+i*8]+" x"+GRID[posK])
      else:
        i+=o
    return False
  elif abs(posD//8-posK//8)==abs(posD%8-posK%8):
    oX=(posD%8>posK%8) - (posD%8<posK%8)
    oY=(posD//8>posK//8) - (posD//8<posK//8)
    i=posD+oX+oY*8
    while i<64 and i>-1:
      if grid[i]!='':
        return isPossible(GRID[i]+' x'+GRID[posK])
      else:
        i+=oX+oY*8
    return False
  return False
    

def kingCheckOK(mov:str)->bool:
  posD,posA=transform_movement(mov)
  strColor=grid[posD][0]
  if kingAlreadyInCheck(strColor,grid):
    if protectsKing(mov):
      return True
  else:
    if not putsKingInCheck(mov):
      return True
  return False

def thereIsPieceAtStartingPoint(mov:str)->bool:
  posD,posA=transform_movement(mov)
  if grid[posD]!='':
    return True

def isLegal(mov:str)->bool:
  if thereIsPieceAtStartingPoint(mov) and isPossible(mov) and kingCheckOK(mov) and noInterference(mov):
    return True
  return False

#DEBUG###########################################################################################
def printGrid(grid):
  for i in range(64):
    print(grid[i],end=" "*(3-len(grid[i])))
    if i%8==7:
      print()
  print()

###TESTS#########################################################################################

grid=[
'','bK','bR','','bQ','bB','','bR',\
'wp','bp','','','bp','bp','bp','bp',\
'','','','','','bN','','',\
'','','','bR','bQ','bB','','',\
'','','','wp','','','','',\
'bp','','wN','','','','','',\
'','wp','wp','','','wp','wp','wp',\
'wR','','wB','wK','wQ','wB','','wR']
def test_transform_movement():
  assert transform_movement("a8 b7")==(0,9)
def test_isPossible():
  #Pawns:
  assert isPossible("b2 b3")
  assert isPossible("b2 b4")
  assert isPossible("d4 xe5")
  assert isPossible("b2 b1")==False

  #Knights:
  assert isPossible("c3 e2")
  assert isPossible("c3 e4")
  assert isPossible("c3 xb5")
  assert isPossible("f6 xg4")
  assert isPossible("f6 g3")==False

  #Bishops:
  assert isPossible("f5 e4")
  assert isPossible("f5 h3")
  assert isPossible("f5 xh2")==False
  assert isPossible("f1 g2")
  assert isPossible("f1 g5")==False

  #Rooks:
  assert isPossible("h1 xa1")
  assert isPossible("a1 a8")
  assert isPossible("a1 h8")==False
  assert isPossible("a1 b2")==False

  #Queens:
  #No need because queen is bishop or rook

  #King:
  assert isPossible("d1 d2")
  assert isPossible("d1 e2")
  assert isPossible("d1 d3")==False
  assert isPossible("d1 c1")
  assert isPossible("d1 b1")==False
def test_noInterference():
  assert noInterference("b8 h2")==False
  assert noInterference("b8 e5")==False
  assert noInterference("b8 d6")
  assert noInterference("a7 a3")
  assert noInterference("a7 a2")==False
def test_kingAlreadyInCheck():
  assert  kingAlreadyInCheck("w",grid)==False
  assert kingAlreadyInCheck("b",grid)
def test_protectsKing():
  assert protectsKing("b8 xa7")
  assert protectsKing("b8 a8")
  assert protectsKing("c8 c7")==False
def test_putsKingInCheck():
  global grid
  assert putsKingInCheck("f2 f4")==False
  assert putsKingInCheck("d4 xe5")
  assert putsKingInCheck("d1 e2")
#No need to test KingCheckOK, it is a simple enough combiation of putsKingInCheck, kingAlreadyInCheck and protectsKing
#No need either to test thereIsAPieceAtStartingPoint, simple function
def test_isLegal():
  assert isLegal("a3 a2")==False
  assert isLegal("a3 xb2")==False
  assert isLegal("a1 xa3")
  assert isLegal("b8 xa7")
  assert isLegal("g2 g3")
  assert isLegal("h1 g1")
