#! /usr/bin/python2
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
from tabulate import tabulate
import sys

url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema') # the schema to import.
imp.filter.add('http://tempuri.org/')

doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor)

username = sys.argv[1]
matricula = client.service.wsConsultaCodigoEstudiante(user = username)
COD_ESTUDIANTE =  matricula.diffgram.NewDataSet.MATRICULA.COD_ESTUDIANTE
print COD_ESTUDIANTE

grades = client.service.wsConsultaCalificaciones(anio = sys.argv[2] , termino =sys.argv[3], estudiante=COD_ESTUDIANTE)

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

print tabulate(grades_table, headers=["MATERIA ","PARCIAL ","FINAL ","MEJORAMIENTO ","PROMEDIO ","ESTADO ","VEZ "])
