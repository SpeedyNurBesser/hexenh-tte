    def clearFilledRows(self):
        lFilledRows = self.lGame.filledRowsExist()
        rFilledRows = self.rGame.filledRowsExist()

        if lFilledRows:
            for row in lFilledRows:
                if row not in self.overlappingHeights:
                    self.lGame.clearRow(row)
                    self.pushBoards(False)
                    lFilledRows.remove(row)

        if rFilledRows:
            for row in rFilledRows:
                if row not in self.overlappingHeights:
                    self.rGame.clearRow(row)
                    self.pushBoards(True)
                    rFilledRows.remove(row)


        if lFilledRows and rFilledRows:
            entirelyFilledRows = list(set(lFilledRows) & set(rFilledRows))
            if entirelyFilledRows != []:
                for row in entirelyFilledRows:
                    self.clearEntireRow(row)