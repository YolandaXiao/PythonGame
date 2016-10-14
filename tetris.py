from Tkinter import *
import random

def init():
    global board
    board=[[canvas.data.emptycolor for col in range(0,canvas.data.cols)] for row in range(0,canvas.data.rows)]
    iPiece = [[ True,  True,  True,  True]]
    jPiece = [[ True, False, False ],
              [ True, True,  True]]
    lPiece = [[ False, False, True],
              [ True,  True,  True]]
    oPiece = [[ True, True],
              [ True, True]]
    sPiece = [[ False, True, True],
              [ True,  True, False ]]
    tPiece = [[ False, True, False ],
              [ True,  True, True]]
    zPiece = [[ True,  True, False ],
              [ False, True, True]]
    tetrisPieces = [ iPiece,jPiece,lPiece,oPiece,sPiece,tPiece,zPiece]
    tetrisPieceColors = [ "#ff0099", "yellow", "#00cc00", "pink", "cyan", "#cc99ff", "orange" ]
    canvas.data.tetrisPieces = tetrisPieces
    canvas.data.tetrisPieceColors = tetrisPieceColors
    canvas.data.score=0
    canvas.data.delay=700
    newFallingPiece()
    
def run(rows,cols):
    global canvas
    root=Tk()
    canvas=Canvas(root,width=360,height=510,bg="#191970")
    canvas.pack()
    root.resizable(width=0,height=0)
    class Struct:pass
    canvas.data=Struct()
    canvas.data.isGameOver=False
    canvas.data.paused=False
    canvas.data.instruct=False
    canvas.data.start=False
    canvas.data.rows=rows
    canvas.data.cols=cols
    canvas.data.cellsize=30
    canvas.data.height=510
    canvas.data.width=360
    canvas.data.xoffset=30
    canvas.data.emptycolor="#6495ed"
    init()
    timeFired()
    root.bind("<Key>", keyPressed)
    root.mainloop()

def redrawAll():
    canvas.delete(ALL)
    if not canvas.data.isGameOver:
        drawGame()
        drawScore()
        if not canvas.data.start:
            menu()
            canvas.data.start=True
        if canvas.data.paused:
            canvas.create_rectangle(0,0,canvas.data.width, canvas.data.height, fill="#6495ed")
            canvas.create_text(40,15,font="Verdana",text="score:"+str(canvas.data.score),fill="white")
            canvas.create_text(180,255,font="Verdana",text="...press c to continue...",fill="white")
# Down - Drop stone faster
# Left/Right - Move stone
# Up - Rotate Stone clockwise
# c - Continue
# P - Pause game
# i - instructions
# space bar - Instant drop
        if canvas.data.instruct:
            canvas.create_rectangle(0,0,canvas.data.width, canvas.data.height, fill="#6495ed")
            canvas.create_text(40,15,font="Verdana",text="score:"+str(canvas.data.score),fill="white")
            canvas.create_text(180,100,font=("Verdana",30),text="INSTURCTIONS",fill="white")
            canvas.create_text(180,140,font="Verdana",text="Down: Drop stone faster",fill="white")
            canvas.create_text(180,160,font="Verdana",text="Left/Right: Move stone",fill="white")
            canvas.create_text(180,180,font="Verdana",text="Up: Rotate Stone counter-clockwise",fill="white")
            canvas.create_text(180,200,font="Verdana",text="Space Bar: Instant drop",fill="white")
            canvas.create_text(180,220,font="Verdana",text="P: Pause",fill="white")
            canvas.create_text(180,240,font="Verdana",text="C: Continue",fill="white")
            canvas.create_text(180,260,font="Verdana",text="I: Instructions",fill="white")
            canvas.create_text(180,280,font="Verdana",text="R: Restart",fill="white")
            canvas.create_text(180,320,font=("Verdana",16),text="choose speed to start",fill="white")
            canvas.create_text(180,340,font=("Verdana",13),text="--press 1 for slow--",fill="white")
            canvas.create_text(180,360,font=("Verdana",13),text="--press 2 for medium--",fill="white")
            canvas.create_text(180,380,font=("Verdana",13),text="--press 3 for fast--",fill="white")
            canvas.create_text(180,400,font=("Verdana",13),text="--press 4 for super fast--",fill="white")


            
    else:
        canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height,fill="#6495ed")
        canvas.create_text(180,240,font=("Verdana",21),text="SCORE  "+str(canvas.data.score),fill="white")
        canvas.create_text(180,180,font=("Verdana",43),text="GAME OVER",fill="white")
        canvas.create_text(180,275,font=("Verdana",14),text="...press r to restart...",fill="white")
        

def drawGame():
    canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height)
    drawBoard()
    drawFallingPiece()

def drawBoard():
    for row in range(canvas.data.rows):
        for col in range(canvas.data.cols):
            drawCell(row,col,board[row][col])

def drawCell(row,col,color):
    canvas.create_rectangle(canvas.data.xoffset+col*canvas.data.cellsize,
                            canvas.data.xoffset+row*canvas.data.cellsize,
                            canvas.data.xoffset+(col+1)*canvas.data.cellsize,
                            canvas.data.xoffset+(row+1)*canvas.data.cellsize,
                            fill=color,width=3,outline="#000080")

def newFallingPiece():
    numberP=int(random.randint(0,6))
    numberC=int(random.randint(0,6))
    canvas.data.piece=canvas.data.tetrisPieces[numberP]
    canvas.data.color=canvas.data.tetrisPieceColors[numberC]
    canvas.data.fallingPieceRow=0
    canvas.data.fallingPieceCol=canvas.data.cols/2-(len(canvas.data.piece[0])/2)
    
def drawFallingPiece():
    for row in range (0,len(canvas.data.piece)):
        for col in range (0,len(canvas.data.piece[0])):
            if canvas.data.piece[row][col]==True:
                drawCell(canvas.data.fallingPieceRow+row,canvas.data.fallingPieceCol+col,canvas.data.color)


def keyPressed(event):
    if(event.keysym == 'Down'):
        moveFallingPiece(1,0)
    elif(event.keysym == 'Left'):
        moveFallingPiece(0,-1)
    elif(event.keysym == 'Right'):
        moveFallingPiece(0,1)
    elif(event.keysym == 'Up'):
        rotateFallingPiece()
    elif(event.keysym == 'space'):
        dropPiece()
    elif(event.keysym == 'p'):
        canvas.data.paused=True
    elif(event.keysym == 'c'):
        canvas.data.paused=False
        canvas.data.instruct=False
    elif(event.keysym == 'i'):
        canvas.data.instruct=True
    elif(event.keysym == '1'):
        canvas.data.delay=1200
        canvas.data.paused=False
        canvas.data.instruct=False
    elif(event.keysym == '2'):
        canvas.data.delay=900
        canvas.data.paused=False
        canvas.data.instruct=False
    elif(event.keysym == '3'):
        canvas.data.delay=600
        canvas.data.paused=False
        canvas.data.instruct=False
    elif(event.keysym == '4'):
        canvas.data.delay=300
        canvas.data.paused=False
        canvas.data.instruct=False
    elif(event.keysym == "r"):
        init()
        canvas.data.isGameOver=False
        canvas.data.paused=False
        canvas.data.instruct=False
    redrawAll()
  
    
def moveFallingPiece(drow,dcol):
    if fallingPieceIsLegal(canvas.data.fallingPieceRow+drow,canvas.data.fallingPieceCol+dcol):
        canvas.data.fallingPieceRow+=drow
        canvas.data.fallingPieceCol+=dcol
        return True
    return False


def fallingPieceIsLegal(newRow,newCol):
    for row in range (0,len(canvas.data.piece)):
        for col in range (0,len(canvas.data.piece[row])):
            if canvas.data.piece[row][col]==True:
                if((newRow+row>=canvas.data.rows) or (newCol+col>=canvas.data.cols)):
                    return False
                elif(0>newCol+col) or (0>newRow+row):
                    return False
                elif(board[newRow+row][newCol+col]!=canvas.data.emptycolor):
                    return False
    return True


 
def rotateFallingPiece():
    fallingPieceRowBackup = canvas.data.fallingPieceRow
    fallingPieceColBackup = canvas.data.fallingPieceCol
    (oldCenterRow, oldCenterCol)=fallingPieceCenter()
    heightToWidth=len(canvas.data.piece)
    widthToHeight=len(canvas.data.piece[0])
    length=widthToHeight
    originalpiece=canvas.data.piece
    canvas.data.piece=rotatePiece(canvas.data.piece)
    (newCenterRow, newCenterCol)=fallingPieceCenter()
    canvas.data.fallingPieceRow+=(oldCenterRow - newCenterRow)
    canvas.data.fallingPieceCol+=(oldCenterCol - newCenterCol)
    if not(fallingPieceIsLegal(canvas.data.fallingPieceRow,canvas.data.fallingPieceCol)):
        canvas.data.piece=originalpiece
        canvas.data.fallingPieceRow = fallingPieceRowBackup
        canvas.data.fallingPieceCol = fallingPieceColBackup

def fallingPieceCenter():
    rowc=(canvas.data.fallingPieceRow+len(canvas.data.piece)/2)
    colc=(canvas.data.fallingPieceCol+len(canvas.data.piece[0])/2)
    return (rowc,colc)

def rotatePiece(piece):
    rotatedPiece=[]
    height=len(piece)
    width=len(piece[0])
    length=width
    for col in range(width):
        cols=[]
        for row in range(height):
            cols.append(piece[row][length-1])
        length-=1
        rotatedPiece.append(cols)
    return rotatedPiece

def timeFired():
    if canvas.data.start:
        if  not canvas.data.isGameOver:
            if not (canvas.data.paused):
                if not (canvas.data.instruct):
                    if not(moveFallingPiece(1,0)):
                        placeFallingPiece()
                        newFallingPiece()
                        removeFullRows()
                        if not(fallingPieceIsLegal(canvas.data.fallingPieceRow,canvas.data.fallingPieceCol)):
                            canvas.data.isGameOver=True
        redrawAll()
    else:
        menu()
    delay=canvas.data.delay
    canvas.after(delay,timeFired)


def placeFallingPiece():
    for row in range (0,len(canvas.data.piece)):
        for col in range (0,len(canvas.data.piece[row])):
            if canvas.data.piece[row][col]==True:
                board[canvas.data.fallingPieceRow+row][canvas.data.fallingPieceCol+col]=canvas.data.color

def removeFullRows():
    sumRows=0
    for oldRow in range(canvas.data.rows-1,-1,-1):
        for col in range(0,canvas.data.cols):
            if(board[oldRow][col]!=canvas.data.emptycolor):
                break
        sumRows=canvas.data.rows-oldRow
    newRow=list()
    for oldRow in range(canvas.data.rows-1,-1,-1):
        for col in range(0,canvas.data.cols):
            if(board[oldRow][col]==canvas.data.emptycolor):
                newRow.append(oldRow)
                break
    sumRowsRemain=len(newRow)
    n=canvas.data.rows-1
    for row in newRow:
        for col in range(0,canvas.data.cols):
            board[n][col]=board[row][col]
        n-=1         
    canvas.data.score+=(sumRows-sumRowsRemain)**2

def drawScore():
    canvas.create_text(40,15,font="Verdana",text="score:"+str(canvas.data.score),fill="white")

def dropPiece():
    n=0
    while(n<canvas.data.rows):
        if fallingPieceIsLegal(canvas.data.fallingPieceRow,canvas.data.fallingPieceCol):
            moveFallingPiece(1,0)
        n+=1

def menu():
    canvas.create_rectangle(0,0,canvas.data.width, canvas.data.height, fill="#6495ed")
    canvas.create_text(180,120,font=("Verdana",60),text="Tetris!",fill="white")
    canvas.create_text(180,480,font=("Verdana",13),text="...Press i for instructions...",fill="white")
    canvas.create_text(180,190,font=("Verdana",16),text="Choose Level to START",fill="white")
    canvas.create_text(180,220,font=("Verdana",13),text="--press 1 for slow--",fill="white")
    canvas.create_text(180,235,font=("Verdana",13),text="--press 2 for medium--",fill="white")
    canvas.create_text(180,250,font=("Verdana",13),text="--press 3 for fast--",fill="white")
    canvas.create_text(180,265,font=("Verdana",13),text="--press 4 for super fast--",fill="white")

        

    
                
    
    

run(15,10)


