class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.rating = []
        
    def add_ratings(self, ratings):
        self.ratings = ratings
        
    def calc_prom(self):
        if self.ratings:
            return (sum(self.ratings)//len(self.ratings))
        else:
            return 0
        
    def approved(self):
        return self.calc_prom() > 61