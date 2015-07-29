#! /usr/bin/python2
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
from tabulate import tabulate
import sys
import os
class Materias():
    def __init__(self):
        self.Materias=[]

    def addMat(self,cod,nombre,paralelo):
        m = [cod,nombre,paralelo]
        self.Materias.append(m)

    def __str__(self):
        return tabulate(self.Materias, headers=["Codigo Materia", "Nombre", "Paralelo" ])

class Horario():
    def __init__(self,Nombre,dia,entrada,salida,aula):
        self.Nombre=Nombre
        self.dia=dia
        self.entrada=entrada
        self.salida=salida
        self.aula=aula

    def __str__(self):
        return "\n\nNombre: "+ self.Nombre + "\nDia: " + self.dia + "\nHora de entrada: " \
        + self.entrada + "\nHora de salida: " + self.salida + "\nAula: " + self.aula

os.system("clear")
url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema') # the schema to import.
imp.filter.add('http://tempuri.org/')

doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor)

username = sys.argv[1]
matricula = client.service.wsConsultaCodigoEstudiante(user = username)
COD_ESTUDIANTE =  matricula.diffgram.NewDataSet.MATRICULA.COD_ESTUDIANTE

MatReg = Materias()
gradesMat = client.service.wsMateriasRegistradas(codigoestudiante= COD_ESTUDIANTE)

for i in gradesMat.diffgram.NewDataSet.MATERIASREGISTRADAS:
    MatReg.addMat(i.COD_MATERIA_ACAD, i.NOMBRE, i.PARALELO)

HorasClase=[]
for i in MatReg.Materias:
    clase = client.service.wsHorarioClases(codigoMateria=i[0],paralelo=i[2]).diffgram.NewDataSet.HORARIOCLASES
    for j in clase:
        horario=Horario(j.NOMBRE, j.NOMBREDIA, j.HORAINICIO, j.HORAFIN, j.AULA)
        HorasClase.append(horario)

for i in HorasClase:
    print (i)
    
input()
print ("\n\n\n\n\n")
#print (tabulate(MatReg.Materias, headers=["Codigo Materia", "Nombre", "Paralelo" ]))
