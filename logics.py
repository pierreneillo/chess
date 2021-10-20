GRID=[chr(i%8+97)+str(8-i//8) for i in range(64)]
grid=['' for i in range(64)]
grid[0]='wB'
grid[4]='wK'
grid[60]='bK'

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

def kingAlreadyInCheck(strColor:str,grid:list=grid)->bool:
  opposite=[]
  if strColor=='w':
    for i in range(len(grid)):
      if 'b' in grid[i]:
        opposite.append(i)
  else:
    for i in range(len(grid)):
      if 'w' in grid[i]:
        opposite.append(i)
  for pos in opposite:
    mov=GRID[pos]+' '+GRID[grid.index(strColor+'K')]
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
  return kingAlreadyInCheck(strColor,tempGrid)
  

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
    opposite=[i for i in range(63) if grid[i][0]==oppColor]
    putsInCkeck=[i for i in opposite if isPossible(i,posK,True) and noInterference(GRID[i]+' x'+GRID[posK])]
    if len(putsInCkeck)!=0:
      print(grid[putsInCkeck[0]],putsInCkeck)
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
      if grid[posD//8+i*8]!='':
        return isPossible(GRID[posD//8+i*8]+" x"+GRID[posK])
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
    

def kingCheckOK(mov:str)->bool:
  posD,posA=transform_movement(mov)
  strColor=grid[posD][0]
  if kingAlreadyInCheck(strColor):
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
print(isLegal('a8 h1'))#True
grid[45]='bp'
print(isLegal('a8 h1'))#False
