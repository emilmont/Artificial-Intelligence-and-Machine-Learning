class Game:
    def __init__(self, game):
        matrix = game['matrix']
        self.n_rows = len(matrix)
        self.n_columns = len(matrix[0])
        
        best = [[None]*self.n_rows, [None]*self.n_columns]
        for row in range(self.n_rows):
            for column in range(self.n_columns):
                p0_val, p1_val = matrix[row][column]
                
                if best[0][row] is None:
                    best[0][row] = (p0_val, column)
                else:
                    p0_val_max, _ = best[0][row]
                    if p0_val > p0_val_max:
                        best[0][row] = (p0_val, column)
                
                if best[1][column] is None:
                    best[1][column] = (p1_val, row)
                else:
                    p1_val_max, _ = best[1][column]
                    if p1_val > p1_val_max:
                        best[1][column] = (p1_val, row)
        
        self.n, self.b, self.s = [], [], [] 
        self.player_names = {}
        for i, player_data in enumerate(game['players']):
            name = player_data[0]
            self.player_names[name] = i
            self.n.append(name)
            self.b.append([index for (_, index) in best[i]])
            self.s.append(player_data[1:])
    
    def dominant_strategy(self, player_name):
        i = self.player_names[player_name]
        best = self.b[i]
        if best.count(best[0]) == len(best):
            return self.s[i][best[0]]
    
    def equilibrium(self):
        equi = []
        for row in range(self.n_rows):
            for column in range(self.n_columns):
                if self.b[0][row] == column and self.b[1][column] == row:
                    equi.append(("%s: %s" % (self.n[0], self.s[0][column]),
                                 "%s: %s" % (self.n[1], self.s[1][row])))
        return equi
