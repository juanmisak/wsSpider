#! /usr/bin/python2
# -*- encoding: utf-8 -*-
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
Data = None
grades_table = []
students = []
name = sys.argv[1]
lastname = sys.argv[2]
anio = sys.argv[3]
termino = sys.argv[4]

name = unicode(name,"utf-8")
lastname = unicode(lastname,"utf-8")
anio = unicode(anio, "utf-8")
termino = unicode(termino,"utf-8")

if name.isalpha() and lastname.isalpha() and anio.isnumeric() and termino.isnumeric:
	Data = client.service.wsConsultarPersonaPorNombres(name,lastname)
	try:
		i = Data[1].__getitem__(0).__getitem__(0)
		i_name = i.NOMBRES
		i_lastname = i.APELLIDOS
		try:
			i_code = i.CODESTUDIANTE
			s=Student(i.NOMBRES, i.APELLIDOS, i.CODESTUDIANTE)
			grades = client.service.wsConsultaCalificaciones(anio, termino, s.idStudent)
			print("\n"+s.name + " " + s.lastname + " " + s.idStudent  + "\n")
		except:
			print("Esta persona no tiene matricula o.O " + i.NOMBRES + " " + i.APELLIDOS)
	except:
		for i in Data.diffgram.NewDataSet.DATOSPERSONA:
			i_name = i.NOMBRES
			i_lastname = i.APELLIDOS
			try:
				i_code = i.CODESTUDIANTE
				students.append(Student(i.NOMBRES, i.APELLIDOS, i.CODESTUDIANTE))
			except:
				#CASOS DE PERSONAS SIN MATRICULA CRISTIAN PEÑAFIEL MANUEL SUAREZ
				print ("\nEsta persona no tiene matricula: " + i.NOMBRES + " " + i.APELLIDOS)
		cont=1
		print ("\n\n\n")
		
		for i in students:
			print (str(cont) + " " + i.name + " " + i.lastname + " " + i.idStudent +"\n" )
			cont+=1

		op=input("Ingrese el numero a consultar: ")
		grades = client.service.wsConsultaCalificaciones(anio, termino, students[int(op)-1].idStudent)


	#try:
		#cal = grades[1].__getitem__(0).__getitem__(0)
		#grade = []
		#grade.append(cal.MATERIA)
		#grade.append(cal.NOTA1)
		#grade.append(cal.NOTA2)
		#grade.append(cal.NOTA3)
		#grade.append(cal.PROMEDIO)
		#grade.append(cal.ESTADO)
		#grade.append(cal.VEZ)
		#grades_table.append(grade)
	#except:
	try:
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
	except:
		print ("No hay calificaciones para el termino " +anio + " " + termino + "\n")

	print (tabulate(grades_table, headers=["MATERIA ","PARCIAL ","FINAL ","MEJORAMIENTO ","PROMEDIO ","ESTADO ","VEZ "],tablefmt="fancy_grid"))
else:
	print ("Entradas invalidas")
