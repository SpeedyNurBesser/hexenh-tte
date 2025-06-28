import json

filename = 'highscores.json'

def loadHighscores():
    try:
        with open(filename, 'r') as file:
            s = file.read().replace('\n', '')
            if not s == '':
                return json.loads(s)
    except:
        pass
    return []

def saveHighscores(highscores):
    with open(filename, 'w') as fout:
        json.dump(highscores, fout)
