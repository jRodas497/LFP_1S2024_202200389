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
                        
    def top3(self):
        sort = sorted(self.students, key = lambda x: x.calc_prom(), reverse=True)[:3]
        with open('top3.html', 'w') as file:
            file.write('<html><head><style>')
            
            file.write('p { margin-bottom: 15px }')
            file.write('</style></head><body><h1>Estudiantes con mejor promdeio</h1>')
            for est in sort:
                
                file.write(f'<p><strong>Carnet:</strong> {est.id}</p>')
                file.write(f'<p><strong>Nombre:</strong> {est.name}</p>')
                file.write(f'<p><strong>Promedio:</strong> {est.calc_prom()}</p><br>')
                
            file.write('</body></html>')
        print('Listado hecho!')
        
    def report(self):
        with open('reporte.html', 'w') as file:
            file.write('<html><head><style>')
            file.write(' h1 { color:navy; }')
            file.write('p { margin-bottom: 15px }')
            file.write('</style></head><body><h1>Reporte de Estudiantes</h1>')
            
            for est in self.students:
                file.write(f'<p><strong>Carnet: </strong> {est.id}</p>')
                file.write(f'<p><strong>Nombre: </strong> {est.name}</p>')
                file.write(f'<p><strong>Carnet: </strong> {est.id}</p>')
                file.write('<p><strong>Calificaciones: </p>')
                file.write(', '.join(map(str, est.rating)))
                file.write('</p><br>')
            file.write('</body></html>')
        print('Listado hecho!')
        
    def approved(self):
        with open('aprobados.html', 'w') as file:
            file.write('')
            file.write('<html><head><style>')
            file.write(' h1 { color:navy; }')
            file.write('p { margin-bottom: 15px }')
            file.write('.approved { color: green, font-weight: bold; }')
            file.write('.not { color: red, font-weight: bold; }')
            file.write('</style></head><body><h1>Reporte de Aprobados</h1>')
            
            for est in self.students:
                file.write(f'<p><strong>Carnet: </strong> {est.id} </p>')
                file.write(f'<p><strong>Nombre: </strong> {est.name} </p>')
                file.write(f'<p><strong>Carnet: </strong> {est.calc_prom()} </p>')
                if est.approved():
                    file.write('<p class = "approved"> Aprobado</p><br>')
                else:
                    file.write('<p class = "not"> Reprobado</p><br>')
            file.write('</body></html>')
        print('Reporte generado!')
            