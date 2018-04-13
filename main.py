#!/usr/bin/env python
import numpy.random as rand
import numpy
import math
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, Plot, Figure, Matrix, NoEscape, Command
from pylatex.utils import italic
import os
# from jinja2 import Template, Environment, FileSystemLoader
# latex_jinja_env = Environment(
# 	block_start_string = '\BLOCK{',
# 	block_end_string = '}',
# 	variable_start_string = '\VAR{',
# 	variable_end_string = '}',
# 	comment_start_string = '\#{',
# 	comment_end_string = '}',
# 	line_statement_prefix = '%%',
# 	line_comment_prefix = '%#',
# 	trim_blocks = True,
# 	autoescape = False,
# 	loader = FileSystemLoader(os.path.abspath('.'))
# )
# template = latex_jinja_env.get_template('jinja-test.tex')


Trigo = [1]*3 + [2]* 2 + [3]*1
Diago = [1]

# Parametres :
shape = Trigo
n = 3



def rand_conf_diag(n):
    r = 0
    l = []
    while r < n-2 :
        k = min(rand.choice(shape), n-r)
        d = rand.choice([1]*10 + [2]*5 + [0]*7 + [-1]*6 + [-2]*6)
        l.append([d,k])
        r = r+k
    while r < n :
        k = min(rand.choice(shape), n-r)
        d = rand.choice([1]*5 + [2]*5 + [3]*4 + [4]*3 + [5]*3 + [0]*7 + [-1]*6 + [-2]*6 + [-3]*2)
        l.append([d,k])
        r = r+k
    l = sorted(l)
    return l

def diag_from_conf(l, n):
    D = numpy.zeros((n,n), dtype=numpy.int64)
    r=0
    for duo in l :
        k = duo[1]
        for i in range(r, r+k-1):
            D[i,i] = duo[0]
            D[i, i+1] = 1
        r = r + k
        D[r-1, r-1] = duo[0]
    return D


def rand_glZ (n):
    a= rand.choice([0]*5 +[1]*3 + [-1]*3 +[2]*2, n*n)
    #a = rand.exponential(3.5/n, n*n).astype(numpy.int64)
    aa = numpy.array(a)
    U = a.reshape(n,n)
    L = aa.reshape(n,n)
    print(U)
    for i in range(0, n) :
        U[i, i] = rand.choice([1, -1])
        L[i, i] = rand.choice([1, -1])
        for j in range(0, i) :
            U[i, j] = 0
            L[j, i] = 0
    P = numpy.dot(L,U)
    return P

def inverse_integer_matrix (P) :
    Pi = numpy.linalg.inv(P)
    Pi_integer = (Pi.round()).astype(numpy.int64)
    return Pi_integer

def latex_matrix (M):
    s = Matrix(M).dumps_content()
    return "\\begin{pmatrix} " + s + "\\end{pmatrix}"


class Jordan_form :

    def __init__(self, n) :
        self.block = rand_conf_diag(n)
        self.jordan = diag_from_conf(self.block, n)
        self.passage = rand_glZ(n)
        self.inverse = inverse_integer_matrix(self.passage)
        self.matrix = numpy.dot(self.passage, numpy.dot(self.jordan, self.inverse))

    def latex_matrix(self) :
        s = latex_matrix(self.matrix)
        return s

    def latex_reduced_matrix(self) :
        sp = latex_matrix(self.passage)
        sj = latex_matrix(self.jordan)
        spi = latex_matrix(self.inverse)
        s = sp + " \cdot " + sj + " \cdot " + spi
        return s




geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
doc = Document(geometry_options=geometry_options,  escape=False)
doc.append('Etudier la diagonalisabilite de la matrice suivante et donner une ecriture sous la forme')
math= Math(data = ["P", Command("cdot D "), Command("cdot P^{-1}")])
doc.append(math)
letter = list('ABC')
for x in letter:
    if x == 'A' :
        l = [[0,3]]
    if x == 'B' :
        l = [[0,2],[0,1]]
    if x == 'C' :
        l = [[0,3]]
    P = rand_glZ(n)
    Pi = numpy.linalg.inv(P)
    Pi = (Pi.round()).astype(numpy.int64)
    D = diag_from_conf(l, n)
    M = numpy.dot(P, numpy.dot(D, Pi))
    doc.append(Math(data=[x, " = ", Matrix(M)]))
    doc.append("Corrige :")
    math = Math(data = ["M =", Matrix(P), Command("cdot"), Matrix(D), Command("cdot"), Matrix(Pi)] )
    doc.append(math)
letter = list('DEFGHJKL')
for x in letter:
    l = rand_conf_diag(n)
    #l =[[3,2]]
    #print l
    P = rand_glZ(n)
    Pi = numpy.linalg.inv(P)
    Pi = (Pi.round()).astype(numpy.int64)
    # print"matrice passage"
    # print(P)
    # print"inverse"
    # print(Pi)
    D = diag_from_conf(l, n)
    # print"diagonale"
    # print(D)
    M = numpy.dot(P, numpy.dot(D, Pi))
    # print"matrice"
    # print(M)
    # print(matrice_to_string(M))
    # Pol = numpy.poly(M)
    # print(Pol)
    # Pol = (numpy.around(Pol)).astype(numpy.int64)
    # print(Pol)
    # print((Matrix(M)))
    # print(Math(data=[Matrix(M)]))
    # print(template.render(matrice=matrice_to_string(M), section2='Short Form'))
    doc.append(Math(data=[x, " = ", Matrix(M)]))
    # doc.append(Command("newpage"))
    doc.append("Corrige :")
    math = Math(data = ["M =", Matrix(P), Command("cdot"), Matrix(D), Command("cdot"), Matrix(Pi)] )
    doc.append(math)
doc.generate_pdf('exo', clean_tex=False)



# doc = Document(geometry_options=geometry_options)
# doc.append(Math(data=[Matrix(M)]))
# doc.append('Le polynome caracteristique est donnee par :')
# i= len(Pol) - 1
# d = " "
# for t in Pol[:n-1]:
#     d = d + " "+ str(t) + "X^"+ str(i) +"+"
#     i = i-1
# d = d + " "+ str(Pol[n-1]) + "X+ " + str(Pol[n])
# d = d.replace("+ -", "-")
# d = d.replace(".0", "")
# d = d.replace(" 1X", " X")
# doc.append(Math(data=[NoEscape(d)]))
#
# doc.append(Math(data=[NoEscape('2\\frac{3}{2}'),"_", 8]))
#
# doc.generate_pdf('corrige', clean_tex=False)
