#! /usr/bin/python

from Tkinter import *

def run():
    global canvas
    root=Tk()
    canvas=Canvas(root,width=700,height=700,bg="#6495ed")
    canvas.pack()
    root.resizable(width=0,height=0)
    class Struct:pass
    canvas.data=Struct()
    canvas.data.isGameOver=False
    canvas.data.win=False
    canvas.data.start=False
    canvas.data.paused=False
    init()
    timeFired()
    root.bind("<KeyPress>", keyPressed)
    root.bind("<KeyRelease>", keyReleased)
    root.bind("<Button-1>", leftMousePressed)
    root.mainloop()

def init():
    canvas.data.cellsize=10
    canvas.data.bgcolor="#6495ed"
    canvas.data.cols=50
    canvas.data.rows=70
    global board
    board=[[canvas.data.bgcolor for col in range(0,canvas.data.cols)] for row in range(0,canvas.data.rows)]
    tpiece=[[True,True,True],
            [False,True,False]]
    ypiece=[[True,False,True],
            [True,True,True],
            [False,True,False]]
    canvas.data.me=[[False,False,True,False,False],
                    [False,True,False,True,False],
                    [True,True,True,True,True],
                    [False,True,False,True,False]]
    canvas.data.boss=[[False,False,True,True,True,False,False],
                     [True,True,True,True,True,True,True],
                     [True,True,False,False,False,True,True],
                     [True,True,True,False,True,True,True],
                     [True,False,True,True,True,False,True],
                     [True,False,False,True,False,False,True]]                     
    canvas.data.finalPiece=[]
    canvas.data.pieces=[tpiece,ypiece]
    initSequence()
    canvas.data.thisPieceRow=50
    canvas.data.thisPieceCol=24

    canvas.data.enemyRow=[]
    canvas.data.enemyCol=[]
    canvas.data.newPieces=[]
# init my bullets
    canvas.data.myBullets=[]
    canvas.data.bullet=[True]
    canvas.data.myBulletRow=canvas.data.thisPieceRow
    canvas.data.myBulletCol=canvas.data.thisPieceCol+2
    canvas.data.myBulletRows=[]
    canvas.data.myBulletCols=[]
# init enemy bullets
    canvas.data.enemyBullets=[[]]
    canvas.data.enemyBulletRow=0
    canvas.data.enemyBulletCol=0
    canvas.data.enemyBulletRows=[[]]
    canvas.data.enemyBulletCols=[[]]
# init boss
    canvas.data.bossRow=0
    canvas.data.bossCol=23
# init boss bullets
    canvas.data.bossBullets=[]
    canvas.data.bossBulletRow=canvas.data.bossRow
    canvas.data.bossBulletCol=canvas.data.bossCol
    canvas.data.bossBulletRows=[]
    canvas.data.bossBulletCols=[]

    canvas.data.count=0
    canvas.data.press=[]
    canvas.data.n=0
    canvas.data.myColor="white"
    canvas.data.enemyColor="white"

    canvas.data.lives=1000
    canvas.data.bossLives=20
    canvas.data.score=0
    canvas.data.fireTime=0
    canvas.data.restart=""
    canvas.data.count2=0
    
#the sequence matches the time(ex.sequence[50]) to the cols of the enemy(ex.27)
def initSequence():
    canvas.data.sequence = [0]*1000
    canvas.data.sequence[50]=27
    canvas.data.sequence[150]=36
    canvas.data.sequence[170]=14
    canvas.data.sequence[190]=40
    canvas.data.sequence[210]=10
    canvas.data.sequence[230]=44
    canvas.data.sequence[250]=6
    canvas.data.sequence[350]=23
    canvas.data.sequence[370]=25
    canvas.data.sequence[390]=27
    canvas.data.sequence[410]=23
    canvas.data.sequence[430]=25
    canvas.data.sequence[530]=20
    canvas.data.sequence[550]=30
    canvas.data.sequence[570]=20
    canvas.data.sequence[590]=30
    canvas.data.sequence[690]=29
    canvas.data.sequence[710]=21
    canvas.data.sequence[900]=25
    
def redrawAll():
    canvas.delete(ALL)
    if not canvas.data.isGameOver:
        if not canvas.data.win:
            drawGame()
            drawLives()
            if not canvas.data.start:
                menu()
                canvas.data.start=True
        else:
            won()
    else:
        GameOver()

def drawGame():
    canvas.create_rectangle(500,0,520,700,fill="white",outline="white")
#drawMe
    drawPieces(canvas.data.me)
#drawEnemy
    drawEnemyPieces()
#drawBullets
    drawMyBullets()
    drawEnemyBullets()
    if canvas.data.count2>=2900:
        drawBoss()
        drawBossBullets()

def drawPiece(row,col,color):
    canvas.create_rectangle(col*canvas.data.cellsize,
                            row*canvas.data.cellsize,
                            (col+1)*canvas.data.cellsize,
                            (row+1)*canvas.data.cellsize,
                            fill=color,outline=color)

def drawPieces(piece):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if(piece[row][col]==True):
                drawPiece(canvas.data.thisPieceRow+row,canvas.data.thisPieceCol+col,canvas.data.myColor)

def drawEnemyPieces():
    for num in range(len(canvas.data.newPieces)):
        for row in range(len(canvas.data.newPieces[num])):
            for col in range(len(canvas.data.newPieces[num][row])):
                if(canvas.data.newPieces[num][row][col]==True):
                    drawPiece(canvas.data.enemyRow[num]+row,canvas.data.enemyCol[num]+col,canvas.data.enemyColor)

def drawBoss():
    for row in range(len(canvas.data.boss)):
        for col in range(len(canvas.data.boss[row])):
            if(canvas.data.boss[row][col]==True):
                drawPiece(canvas.data.bossRow+row,canvas.data.bossCol+col,"white")


def drawMyBullets():
    for n in range(len(canvas.data.myBullets)):
        drawPiece(canvas.data.myBulletRows[n],canvas.data.myBulletCols[n],"aquamarine")

def drawEnemyBullets():
 #   print "enemyrow: %i" % len(canvas.data.enemyRow)
    for num in range(len(canvas.data.enemyRow)):
        for n in range(len(canvas.data.enemyBulletRows[num])):
            drawPiece(canvas.data.enemyBulletRows[num][n],canvas.data.enemyBulletCols[num][n],"yellow")

def drawBossBullets():
    for n in range(len(canvas.data.bossBullets)):
        drawPiece(canvas.data.bossBulletRows[n],canvas.data.bossBulletCols[n],"orange")

def moveEnemyPiece(drow,dcol):
    flag= False
#    print (canvas.data.enemyRow,canvas.data.enemyCol)
    for num in range(len(canvas.data.newPieces)):
#        if enemyIsLegal(canvas.data.newPieces[num],canvas.data.enemyRow[num]+drow,canvas.data.enemyCol[num]+dcol):
        canvas.data.enemyRow[num]+=drow
        canvas.data.enemyCol[num]+=dcol
        flag=  True
    return flag

def moveMe(drow,dcol):
    if thisPieceIsLegal(canvas.data.me,canvas.data.thisPieceRow+drow,canvas.data.thisPieceCol+dcol):
        canvas.data.thisPieceRow+=drow
        canvas.data.thisPieceCol+=dcol
        return True
    return False

def moveBoss(n):
#    if thisPieceIsLegal(canvas.data.boss,canvas.data.bossRow+1,canvas.data.bossCol):
    if n<=2925:
        canvas.data.bossRow+=1
    elif(n>2925):
        if n==2926:
            canvas.data.bossCol+=1
        if n%50==0:
            canvas.data.bossCol+=2
        elif n%25==0:
            canvas.data.bossCol-=2
        

def thisPieceIsLegal(piece,newRow,newCol):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if(piece[row][col]==True):
                if(0>newCol+col)or (newCol+col>=canvas.data.cols):
                    return False
                elif(0>newRow+row) or (newRow+row>=canvas.data.rows):
                    return False
    return True

def keyPressed(event):
    if(event.keysym == 'Down'):
        canvas.data.press.append("Down")
    elif(event.keysym == 'Left'):
        canvas.data.press.append("Left")
    elif(event.keysym == 'Right'):
        canvas.data.press.append("Right")
    elif(event.keysym == 'Up'):
        canvas.data.press.append("Up")
    elif(event.keysym == "r"):
        init()
        canvas.data.isGameOver=False
        canvas.data.paused=False
        canvas.data.start=True
        canvas.data.win=False
    elif(event.keysym == "p"):
        canvas.data.paused=True
    elif(event.keysym == "c"):
        canvas.data.paused=False
        

def keyReleased(event):
    if(event.keysym == 'Down'):
        canvas.data.press.remove("Down")
    elif(event.keysym == 'Left'):
         canvas.data.press.remove("Left")
    elif(event.keysym == 'Right'):
        canvas.data.press.remove("Right")
    elif(event.keysym == 'Up'):
        canvas.data.press.remove("Up")

def leftMousePressed(event):
    if event.x>=180 and event.x<=290:
        if event.y<=490 and event.y>=450:
            canvas.data.start=True
            canvas.create_rectangle(180,450,290,490,fill="#6495ed",outline="white")
            redrawAll()

def timeFired():
    if canvas.data.start:
        if  not canvas.data.isGameOver:
            if not canvas.data.win:
                if not (canvas.data.paused):
                    #key pressed
                    keyPress()
                    if canvas.data.fireTime%300==0:
                        newEnemyBullets()
                    if canvas.data.fireTime%250==0:
                        newBossBullets()
                    if canvas.data.fireTime%150==0:
                        newBullets()
                    canvas.data.fireTime+=5
                    moveMyBullets()
                    moveEnemyBullets()
                    moveBossBullets()
    
                    moveEnemyPiece(1,0)
                    newEnemyPiece(canvas.data.count)
    

                    if canvas.data.count2>=2900:
                        moveBoss(canvas.data.count2)
                        shotByBoss()
                        shotBoss()
                
                    shotEnemy()
                    if collision():
                        canvas.data.myColor="red"
                    elif gettingShot():
                        canvas.data.myColor="red"
                    else:
                        canvas.data.myColor="white"

                    canvas.data.count+=1
                    canvas.data.count2+=1
                    if canvas.data.count>=1000:
                        canvas.data.count=0
                    removeThings()
                    

                    
                    collideBoss()
                    if canvas.data.lives<=0:
                        canvas.data.isGameOver=True
                    if canvas.data.bossLives<=0:
                        canvas.data.win=True
        redrawAll()
    else:
        menu()
    delay=20
    canvas.after(delay,timeFired)

def newEnemyPiece(n):
    if canvas.data.sequence[n]!=0:
        if(n>=350 and n<=430):
            canvas.data.newPieces.append(canvas.data.pieces[0])
        else:
            canvas.data.newPieces.append(canvas.data.pieces[1])
        canvas.data.enemyRow.append(0)
        canvas.data.enemyCol.append(canvas.data.sequence[n])


def collision():
    flag=False
    num=0
    while(num<=len(canvas.data.newPieces)-1):
        sign=False
        for row in range(len(canvas.data.newPieces[num])):
            for col in range(len(canvas.data.newPieces[num][row])):
                if(canvas.data.newPieces[num][row][col]==True):
                    for r in range(len(canvas.data.me)):
                        for c in range(len(canvas.data.me[0])):
                            if(canvas.data.me[r][c]==True):
                                if(canvas.data.enemyRow[num]+row==canvas.data.thisPieceRow+r) and (canvas.data.enemyCol[num]+col==canvas.data.thisPieceCol+c):
                                    canvas.data.newPieces.remove(canvas.data.newPieces[num])
                                    canvas.data.enemyRow.remove(canvas.data.enemyRow[num])
                                    canvas.data.enemyCol.remove(canvas.data.enemyCol[num])
                                    canvas.data.lives-=1
#                                    num=len(canvas.data.newPieces)-1
                                    sign=True
                                    flag=True
                                    break
                        if(sign==True):
                            break
                    if(sign==True):
                        break
            if(sign==True):
                break 
        if(sign==False):                        
            num+=1
    return flag

def collideBoss():
    sign=False
    for row in range(len(canvas.data.boss)):
        for col in range(len(canvas.data.boss[row])):
            if(canvas.data.boss[row][col]==True):
                for r in range(len(canvas.data.me)):
                    for c in range(len(canvas.data.me[0])):
                        if(canvas.data.me[r][c]==True):
                            if(canvas.data.bossRow+row==canvas.data.thisPieceRow+r) and (canvas.data.bossCol+col==canvas.data.thisPieceCol+c):
                                if canvas.data.count2>=2900:
                                    canvas.data.me=[]
                                    canvas.data.isGameOver=True
                                    sign=True
                                    break
                    if(sign==True):
                        break
                if(sign==True):
                    break
        if(sign==True):
            break                        

def newBullets():
    canvas.data.myBulletRow=canvas.data.thisPieceRow
    canvas.data.myBulletCol=canvas.data.thisPieceCol+2
    canvas.data.myBullets.append(canvas.data.bullet)
    canvas.data.myBulletRows.append(canvas.data.myBulletRow)
    canvas.data.myBulletCols.append(canvas.data.myBulletCol)

def newEnemyBullets():
    for num in range(len(canvas.data.enemyRow)):
        canvas.data.enemyBulletRow=canvas.data.enemyRow[num]
        canvas.data.enemyBulletCol=canvas.data.enemyCol[num]
        canvas.data.enemyBullets[num].append(canvas.data.bullet)
        canvas.data.enemyBullets.append(canvas.data.enemyBullets[num])
#        canvas.data.enemyBulletRows[num].append(canvas.data.emyBulletRownemyBulletRow)
#        canvas.data.enemyBulletCols[num].append(canvas.data.enemyBulletCol)
        canvas.data.enemyBulletRows[num].append(canvas.data.enemyBulletRow)
        canvas.data.enemyBulletRows.append(canvas.data.enemyBulletRows[num])
        canvas.data.enemyBulletCols[num].append(canvas.data.enemyBulletCol+1)
        canvas.data.enemyBulletCols.append(canvas.data.enemyBulletCols[num])        
        

def newBossBullets():
    canvas.data.bossBulletRow=canvas.data.bossRow+3
    canvas.data.bossBulletCol=canvas.data.bossCol+4
    canvas.data.bossBullets.append(canvas.data.bullet)
    canvas.data.bossBulletRows.append(canvas.data.bossBulletRow)
    canvas.data.bossBulletCols.append(canvas.data.bossBulletCol)

def moveMyBullets():
    for n in range(len(canvas.data.myBullets)):
        canvas.data.myBulletRows[n]+=-2

def moveEnemyBullets():
    for num in range(len(canvas.data.enemyRow)):
        for n in range(len(canvas.data.enemyBulletRows[num])):
            canvas.data.enemyBulletRows[num][n]+=2

def moveBossBullets():
    for n in range(len(canvas.data.bossBullets)):
        canvas.data.bossBulletRows[n]+=2           


def shotEnemy():
    num=0
    #print "shot len:%i" % len(canvas.data.newPieces)
    while(num<=len(canvas.data.newPieces)-1):   
        #print ("num: %i" %(num))
        sign=False
        for row in range(len(canvas.data.newPieces[num])):
            for col in range(len(canvas.data.newPieces[num][row])):
                if(canvas.data.newPieces[num][row][col]==True):
                    for n in range(len(canvas.data.myBullets)):
                        #print ("row: %i %i  %i"  %(n, canvas.data.myBulletRows[n], canvas.data.enemyRow[num]+row))
                        #print ("col: %i %i  %i"  %(n, canvas.data.myBulletCols[n], canvas.data.enemyCol[num]+col))
                        for scope in range(row-2, row+2):
                            if (canvas.data.enemyRow[num]+scope)==canvas.data.myBulletRows[n] and (canvas.data.enemyCol[num]+col)==canvas.data.myBulletCols[n]:
                                canvas.data.newPieces.remove(canvas.data.newPieces[num])
                                canvas.data.enemyRow.remove(canvas.data.enemyRow[num])
                                canvas.data.enemyCol.remove(canvas.data.enemyCol[num])
                                canvas.data.score+=1
                                sign=True
                                #print "ok"
                                break;
                        if(sign==True):
                            break;
                    if(sign==True):
                        break; 
            if(sign==True):
                break;     
        if(sign==False):
            num+=1

def gettingShot():
    for num in range(len(canvas.data.enemyRow)):
        for n in range(len(canvas.data.enemyBulletRows[num])):
            for row in range(len(canvas.data.me)):
                for col in range(len(canvas.data.me)):
                    if(canvas.data.me[row][col]==True):
                        if canvas.data.enemyBulletRows[num][n]==canvas.data.thisPieceRow+row and canvas.data.enemyBulletCols[num][n]==canvas.data.thisPieceCol+col:
                            canvas.data.lives-=1
                            canvas.data.enemyBullets[num].remove(canvas.data.enemyBullets[num][n])
                            canvas.data.enemyBulletRows[num].remove(canvas.data.enemyBulletRows[num][n])
                            canvas.data.enemyBulletCols[num].remove(canvas.data.enemyBulletCols[num][n])
                            return True
    return False

def shotBoss():
    sign=False
    for row in range(len(canvas.data.boss)):
            for col in range(len(canvas.data.boss[row])):
                if(canvas.data.boss[row][col]==True):
                    for n in range(len(canvas.data.myBullets)):
#                        for scope in range(row-2, row+2):
                        if (canvas.data.bossRow+row)==canvas.data.myBulletRows[n] and (canvas.data.bossCol+col)==canvas.data.myBulletCols[n]:
                            canvas.data.bossLives-=1
                            canvas.data.myBullets.remove(canvas.data.myBullets[n])
                            canvas.data.myBulletRows.remove(canvas.data.myBulletRows[n])
                            canvas.data.myBulletCols.remove(canvas.data.myBulletCols[n])
                            sign=True
                            break;
                        if(sign==True):
                            break;
                    if(sign==True):
                        break; 
            if(sign==True):
                break;

def shotByBoss():
    for row in range(len(canvas.data.me)):
        for col in range(len(canvas.data.me[row])):
            if canvas.data.me[row][col]==True:
                for n in range(len(canvas.data.bossBullets)):
                    if canvas.data.bossBulletRows[n]==canvas.data.thisPieceRow+row and canvas.data.bossBulletCols[n]==canvas.data.thisPieceCol+col:
                        canvas.data.lives-=1
                        
    

def drawLives():
    canvas.create_text(580,40,font=("Verdana",18),text="Lives:"+str(canvas.data.lives),fill="white")
#    canvas.create_text(600,50,font=("Verdana",18),text="bossLives:"+str(canvas.data.bossLives),fill="white")
    canvas.create_text(577,80,font=("Verdana",18),text="Score:"+str(canvas.data.score),fill="white")

def menu():
    canvas.create_rectangle(0,0,700,700, fill="#6495ed")
    canvas.create_text(235,150,font=("Verdana",65),text="Invader!",fill="white")
    canvas.create_rectangle(500,0,520,700,fill="white",outline="white")

    canvas.create_text(235,300,font=("Verdana",16),text="Instructions",fill="white")
    canvas.create_text(235,340,font=("Verdana",13),text="--press r to start/restart--",fill="white")
    canvas.create_text(235,360,font=("Verdana",13),text="--press p to pause--",fill="white")
    canvas.create_text(235,380,font=("Verdana",13),text="--press c to continue--",fill="white")
#    canvas.create_rectangle(180,450,290,490,fill="#6495ed",outline="white",width="3")
    canvas.create_text(235,470,font=("Verdana",40),text="start",fill="white")
    canvas.create_text(235,510,font=("Verdana",13),text="...click Start...",fill="white")
    drawLives()

    

def GameOver():
    canvas.create_rectangle(0,0,700,700, fill="#6495ed")
    canvas.create_text(235,150,font=("Verdana",60),text="Game Over!",fill="white")
    canvas.create_rectangle(500,0,520,700,fill="white",outline="white")
    canvas.create_text(235,220,font=("Verdana",40),text="Score:"+str(canvas.data.score),fill="white")
    canvas.create_text(235,280,font=("Verdana",20),text="--press r to restart--",fill="white")
    drawLives()

def won():
    canvas.create_rectangle(0,0,700,700, fill="#6495ed")
    canvas.create_text(235,300,font=("Verdana",40),text="You defeat",fill="white")
    canvas.create_text(235,380,font=("Verdana",60),text="the boss!",fill="white")
    canvas.create_text(235,150,font=("Verdana",40),text="Score:"+str(canvas.data.score),fill="white")
    canvas.create_rectangle(500,0,520,700,fill="white",outline="white")
    canvas.create_text(235,500,font=("Verdana",20),text="--press r to restart--",fill="white")
    drawLives()


def removeThings():
    num=0
    while num<=len(canvas.data.enemyRow)-1:
        if canvas.data.enemyRow[num]>=canvas.data.rows:
            canvas.data.newPieces.remove(canvas.data.newPieces[num])
            canvas.data.enemyRow.remove(canvas.data.enemyRow[num])
            canvas.data.enemyCol.remove(canvas.data.enemyCol[num])
        else:
            num+=1
    num=0
    while num<=len(canvas.data.myBulletRows)-1:
        if canvas.data.myBulletRows[num]<0:
            canvas.data.myBullets.remove(canvas.data.myBullets[num])
            canvas.data.myBulletRows.remove(canvas.data.myBulletRows[num])
            canvas.data.myBulletCols.remove(canvas.data.myBulletCols[num])
        else:
            num+=1
    num=0
    while num<=len(canvas.data.enemyBulletRows)-1:
        n=0
        sign=False
        while n<=(len(canvas.data.enemyBulletRows[num])-1):
            if canvas.data.enemyBulletRows[num][n]>=canvas.data.rows:
                canvas.data.enemyBullets[num].remove(canvas.data.enemyBullets[num][n])
#                canvas.data.enemyBullets.remove(canvas.data.enemyBullets[num])
                canvas.data.enemyBulletRows[num].remove(canvas.data.enemyBulletRows[num][n])
#                canvas.data.enemyBulletRows.remove(canvas.data.enemyBulletRows[num])
                canvas.data.enemyBulletCols[num].remove(canvas.data.enemyBulletCols[num][n])
                sign=True
#                canvas.data.enemyBulletCols.remove(canvas.data.enemyBulletCols[num])
            else:
                n+=1               
        if(sign==False):
            num+=1
    num=0
    while num<=len(canvas.data.bossBulletRows)-1:
        if canvas.data.bossBulletRows[num]>=canvas.data.rows:
            canvas.data.bossBullets.remove(canvas.data.bossBullets[num])
            canvas.data.bossBulletRows.remove(canvas.data.bossBulletRows[num])
            canvas.data.bossBulletCols.remove(canvas.data.bossBulletCols[num])
        else:
            num+=1

def keyPress():
    for var in canvas.data.press:
        if(var=="Down"):
            moveMe(1,0)
        if(var=="Up"):
            moveMe(-1,0)
        if(var=="Right"):
            moveMe(0,1)
        if(var=="Left"):
            moveMe(0,-1)
       

run()
