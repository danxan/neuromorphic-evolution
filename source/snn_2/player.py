
class Player:
    def activate(self, bs):
        a = getch.getch()
        if a == 'h':
            return [1,0]
        if a == 'j':
            return [1,1]
        if a == 'k':
            return [0,0]
        if a == 'l':
            return [0,1]


