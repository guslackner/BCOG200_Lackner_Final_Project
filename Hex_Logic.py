class DisjointSet:
    #disjoint set termination method adapted from https://www.youtube.com/watch?v=QYivmB3B7S0
    def __init__(self, elems):
        self.elems = elems
        self.parent = {}
        self.size = {}
        for elem in elems:
            self.make_set(elem)

    def make_set(self, x):
        self.parent[x] = x
        self.size[x] = 1

    def find(self, x):
        if self.parent[x] == x:
            return x
        else:
            self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        elif self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

class Gameboard:
    def __init__(self, n=11):
        self.n = n
        self.board = [[0]*n for _ in range(n)]
        self.cells = [(i, j) for i in range(n) for j in range(n)]
        self.top_node = (-1, 0)
        self.bottom_node = (n, 0)
        self.left_node = (0, -1)
        self.right_node = (0, n)

        #calculate set collections for each color
        self.red_disjoint_set = DisjointSet(self.cells + [self.top_node, self.bottom_node])
        self.blue_disjoint_set = DisjointSet(self.cells + [self.left_node, self.right_node])

        for i in range(n):
            self.red_disjoint_set.union((0, i), self.top_node)
            self.blue_disjoint_set.union((i,0), self.left_node)
            self.red_disjoint_set.union(((n-1), i), self.bottom_node)
            self.blue_disjoint_set.union((i, (n-1)), self.right_node)

    def play(self, i, j, player):
        #check for invalid input and illegal moves
        assert 0 <= i < self.n and 0 <= i < self.n and self.board[i][j] == 0 
        #change player into a number
        player_number = 1 if player == 'red' else 2
        self.board[i][j] = player_number
        for neighbor_i, neighbor_j in [(i + 1, j), (i + 1, j - 1), (i, j+1), (i, j-1), (i-1, j), (i-1, j+1)]:
            if 0 <= neighbor_i < self.n and 0 <= neighbor_j < self.n and player_number == self.board[neighbor_i][neighbor_j]:
                if player == 'red':
                    self.red_disjoint_set.union((neighbor_i, neighbor_j), (i, j))
                else:
                    self.blue_disjoint_set.union((neighbor_i, neighbor_j), (i, j))
        if self.red_disjoint_set.find(self.top_node) == self.red_disjoint_set.find(self.bottom_node):
            return 'red wins'
        elif self.blue_disjoint_set.find(self.left_node) == self.blue_disjoint_set.find(self.right_node):
            return 'blue wins'
            
    def print_board(self):
        viz = ''
        cap = ''
        base = ''
        for index in range(self.n):
            cap  += " / \\"
            #base += " \ /"
        base =  " \\" + cap
        viz += cap + "\n"
        cap += " /"
        row = ' |'
        for i in range(self.n):
            row = '| '
            for j in range(self.n):
                row += str(self.board[i][j]) + ' | '
            viz +=  "  "*i + row + "\n"
            viz += "  "*i + base + "\n"
        print(viz[:-2])
        
        
        


if __name__ == "__main__":
    print("Instructions\n Player1 aka 'red' should try to connect the top of the game board with the bottom.\n Player2 aka 'blue' should try to connect the left to the right side.\n You can claim one unoccupied square per turn.\n Whoever succeads wins. ")
    board = Gameboard()
    p = 1
    winner = None
    while winner is None:
        print(board.print_board())
        print(board.board)
        row_index = int(input("   Input row: ")) -1
        col_index = int(input("Input column: ")) -1
        p = (p + 1)%2
        player = 'red' if p == 0 else 'blue'
        winner = board.play(row_index, col_index, player)
    print(winner)
        