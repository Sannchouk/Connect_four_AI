from game import *

def test_diagonal():
    b = Connect_four()
    b.board = [[0,0,0,0], [-1.,  0.,  0.,  0.,],[-1., -1.,  0.,  0.],[ 1.,  1., -1.,  0.],[ 1.,  1.,  1., -1.,],]
    print(b.diagonal2(3, 2, -1))
    b.display()

    b.board = [[0,0,0,0], [0,  0.,  0.,  1,],[0, -1.,  1., 0],[ 1.,  1., -1.,  1],[ 1.,  1.,  0, 1,],]
    print(b.diagonal1(2, 2, 1))
    b.display()

    b.board =  [[-1, -1, -1,  1,], [-1, -1,  1,  0,],[ 1,  1, -1,  1,],[ 1, -1,  1, -1,],[ 1,  1,  1, -1,]]
    print(b.diagonal1(1, 2, 1))
    b.display()

    b.board = [[ 0,  0,  0,  0,],
 [-1,  0,  0,  0,],
 [-1, -1, -1,  1,],
 [ 1,  1, -1,  1,],
 [ 1,  1,  1, -1,]]
    print(b.diagonal2(4, 3, -1))
    b.display()

    b.board = [[-1, -1,  0,  0,],
 [-1,  0,  0,  0,],
 [-1, -1,  1,  1,],
 [ 1,  1, -1,  1,],
 [ 1,  1,  1, -1,]]
    print(b.diagonal2(4, 3, -1) or b.diagonal1(4, 3, -1))
    b.display()

test_diagonal()
