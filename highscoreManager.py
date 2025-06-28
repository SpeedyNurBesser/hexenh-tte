import json

filename = 'highscores'

def loadHighscores():
    s = []
    with open(filename, 'r') as file:
        s = file.read().replace('\n', '')
    if s == '':
        return []
    return json.loads(s)

def saveHighscores(highscores):
    with open(filename, 'w') as fout:
        json.dump(highscores, fout)
