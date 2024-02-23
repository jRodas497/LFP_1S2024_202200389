from Student import Student

class School:
    def __init__(self):
        self.students = []
        
    def load_students(self, nFile):
        with open(nFile, 'r') as f:
            for l in f:
                id, name = l.strip().split(':')
                self.students.append(Student(id, name.strip('"')))
        print('###   Estudiantes añadidos   ###')
    
    def add_ratings(self, nFile):
        with open(nFile, 'r') as f:
            for l in f:
                id, ratings = l.strip().split(':')
                ratings = list(map(int, ratings.split(',')))
                for student in self.students:
                    if student.id == id:
                        student.add_ratings(ratings)
                        
    