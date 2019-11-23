
class Fluid:
    def __init__(self, R=289.8, k=1.4):
        self.R = R
        self.k = k

    def get_ro(self, p, T):
        p = p
        return p / (self.R * T)




