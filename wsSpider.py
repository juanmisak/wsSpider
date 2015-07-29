#! /usr/bin/python2
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
from tabulate import tabulate
import sys

class Student():
	def __init__(self, name, lastname, idStudent):
		self.name = name
		self.lastname = lastname
		self.idStudent = idStudent

	def __str__(self):
		return " " + self.name + " " + self.lastname

url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema') # the schema to import.
imp.filter.add('http://tempuri.org/')

doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor)

name = sys.argv[1]
lastname = sys.argv[2]

Data = client.service.wsConsultarPersonaPorNombres(nombre = name,apellido = lastname)
students = []
try:
	i = Data[1].__getitem__(0).__getitem__(0)
	s=Student(i.NOMBRES, i.APELLIDOS, i.CODESTUDIANTE)
	grades = client.service.wsConsultaCalificaciones(anio = sys.argv[3], termino =sys.argv[4], estudiante=i.CODESTUDIANTE)
	print("\n" + str(s) + "\n")
except:

		try:
			for i in Data[1].__getitem__(0).__getitem__(0):
				students.append(Student(i.NOMBRES, i.APELLIDOS, i.CODESTUDIANTE))

			cont=1
			for i in students:

				print ("\n" + str(cont) + str(i))
				cont+=1
			print ("\n")

			op=input("Ingrese el nombre a consultar: ")
			grades = client.service.wsConsultaCalificaciones(anio = sys.argv[3], termino =sys.argv[4], estudiante=students[int(op)-1].idStudent)

		except:
			print ("")


grades_table = []
for cal in grades.diffgram.NewDataSet.CALIFICACIONES:
	grade = []
	grade.append(cal.MATERIA)
	grade.append(cal.NOTA1)
	grade.append(cal.NOTA2)
	grade.append(cal.NOTA3)
	grade.append(cal.PROMEDIO)
	grade.append(cal.ESTADO)
	grade.append(cal.VEZ)
	grades_table.append(grade)

print (tabulate(grades_table, headers=["MATERIA ","PARCIAL ","FINAL ","MEJORAMIENTO ","PROMEDIO ","ESTADO ","VEZ "],tablefmt="fancy_grid"))
