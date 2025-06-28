for y, _ in enumerate(self.board[0]):
            filledSlots = 0
            for x in range(len(self.board)):
                if self.board[x][y] == OCCUPIED_SYMBOL:
                    filledSlots += 1
            
            if filledSlots == len(self.board):
                filledRows.append(y)