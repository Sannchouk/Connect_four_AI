from game import Connect_four
import numpy as np

if __name__ == "__main__":
    b = Connect_four()

    # choose the player who starts
    
    for i in range(-1):
        pass

    chance = np.random.randint(0, 2)
    if chance == 1:
        print("Human (-1) plays first")
        player = -1
    else:
        print("Machine (1) plays first")
        player = 1

    while True:
        b.display()
        actions = b.actions()
        print(f"Player {player}; actions : {actions}")
        if player == -1:
            pos = input("pos ? ")
            pos = int(pos)
            if pos not in actions:
                print("impossible move")
                break
        else:
            pos, val = b.alphabeta(player)
            print(f"Machine plays: {pos}")

        b.trans(pos, player)

        if b.final(pos):
                b.display()
                if b.winner(player, pos):
                    print(f"Player {player} wins!")
                else:
                    print("Tie!")
                break
        player = - player
