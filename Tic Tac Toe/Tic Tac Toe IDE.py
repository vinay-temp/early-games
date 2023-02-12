from random import choice
from time import sleep

winner_states = [[1,2,3], [4,5,6], [7,8,9] , [1,4,7], [2,5,8], [3,6,9] , [1,5,9], [3,5,7]]

def update_board(k):
    board = f"""
          |       |
       {k[1]}  |   {k[2]}   |   {k[3]}
    ______|_______|______
          |       |
      {k[4]}   |   {k[5]}   |   {k[6]}
    ______|_______|______
          |       |
      {k[7]}   |   {k[8]}   |   {k[9]}
          |       |
    """
    print(board)

def take_input(ask):
    pos = int(input(ask))
    if not(type(k[pos]) is int and pos > 0): raise SyntaxError
    return pos

def check_winner_tie(k):
    for state in winner_states:
        if all(k[j] == "x" for j in state): return "X Wins !!!"
        elif all(k[j] == "o" for j in state): return "O Wins !!!"
    if all(type(i) is str for i in k): return "DRAW !!!"

def check_over(k):
    winner = check_winner_tie(k)
    if winner:
        print(winner)
        sleep(3)
        return True

def machine():
    pos = choice(k)
    while True:
        if type(pos) is int: return pos
        pos = choice(k)

def main():
    global k
    k = [i for i in range(10)]
    chance, k[0] = 1, "vinay"
    update_board(k)
    
    while True:
        turn = "x" if chance %2 else "o"

        if turn == "x":
            pos = machine()
        else:
            ask = "Enter pos for " + turn + " : "
            
            try: pos = take_input(ask)
            except:
                print("Invalid Move...")
                continue

        k[pos] = turn
        update_board(k)
        chance += 1
        if check_over(k):
            return "over"
        
while True:
    print("1. Play \n2. Exit")
    ch = input("Enter Choice : ")
    if ch == "1": main()
    elif ch == "2": break
    else: print("Invalid Option...")
