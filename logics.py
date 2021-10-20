from math import *
GRID=[chr(i%8+97)+str(8-i//8) for i in range(64)]
grid=['' for i in range(64)]
grid[0]='wB'

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

def isPossibleTower(posD:int,posA:int,eat:bool)->bool:
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
  elif piece=='T':
    return isPossibleTower(posD,posA,eat)
  elif piece=='B':
    return isPossibleBishop(posD,posA,eat)
  elif piece=='Q':
    return isPossibleTower(posD,posA,eat) or isPossibleBishop(posD,posA,eat)
  elif piece=='K':
    return isPossibleKing(posD,posA,eat)
  elif piece=='p':
    return isPossiblePawn(posD,posA,eat,strColor)

def noInterference(mov:str)->bool:
  posD,posA=transform_movement(mov)
  eat='x' in mov
  if abs(posA//8-posD//8)<=1 and abs(posA%8-posD%8)<=1:
    return True
  if isPossibleTower(posD,posA,eat):
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

def kingAlreadyInCheck(strColor:str)->bool:
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
  pass

def kingCheckOK(mov:str)->bool:
  posD,posA=transform_movement(mov)
  eat='x' in mov
  piece,strColor=grid[posD][1],grid[posD][0]
  if kingAlreadyInCheck(strColor):
    if protectsKing(mov):
      return True
  else:
    if not putsKingInCheck(mov):
      return True

def thereIsPieceAtStartingPoint(mov:str)->bool:
  posD,posA=transform_movement(mov)
  if grid[posD]!='':
    return True

def isLegal(mov:str)->bool:
  if thereIsPieceAtStartingPoint(mov) and isPossible(mov) and kingCheckOK(mov):
    return True
print(isLegal('a8 h1'))
grid[45]='bp'
print(isLegal('a8 h1'))
