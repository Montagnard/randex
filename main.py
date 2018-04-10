import numpy.random as rand
import numpy
import math
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, NoEscape
from pylatex.utils import italic
import os
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
latex_jinja_env = Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = FileSystemLoader(os.path.abspath('.'))
)
template = latex_jinja_env.get_template('jinja-test.tex')
n = 3
def rand_glZ (n):
    a = rand.exponential(2, n*n).astype(numpy.int64)
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

P = rand_glZ(n)
Pi = numpy.linalg.inv(P)
Pi = Pi.astype(numpy.int64)
print"matrice passage"
print(P)
print"inverse"
print(Pi)

Trigo = [1]*3 + [2]* 2 + [3]*1
Diago = [1]

def rand_conf_diag(n):
    r = 0
    l = []
    while r < n :
        k = min(rand.choice(Diago), n-r)
        d = rand.choice([1]*10 + [2]*5 + [3]*4 + [4]*3 + [5] + [0]*7 + [-1]*6 + [-2]*6 + [-3]*2)
        l.append([k,d])
        r = r+k
    return l

l =[[3,2]]
print l
def diag_from_conf(l, n):
    D = numpy.zeros((n,n), dtype=numpy.int64)
    r=0
    for duo in l :
        k = duo[0]
        for i in range(r, r+k-1):
            D[i,i] = duo[1]
            D[i, i+1] = 1
        r = r + k
        D[r-1, r-1] = duo[1]
    return D

D = diag_from_conf(l, n)

M = numpy.dot(P, numpy.dot(D, Pi))
print"diagonale"
print(D)
print"matrice"
print(M)
def matrice_to_string(M):
    s = "\[ \\begin{pmatrix}"
    for ligne in M[:-1]:
        for x in ligne[:-1]:
            s = s + str(x) + "&"
        s = s + str(ligne[-1])
        s = s + "\\\\"
    for x in M[-1][:-1]:
        s = s + str(x) + "&"
        s = s + str(M[-1][-1])
    s = s + "\\end{pmatrix} \]"
    return s

print(matrice_to_string(M))
Pol = numpy.poly(M)
print(Pol)
Pol = (numpy.around(Pol)).astype(numpy.int64)
print(Pol)
print((Matrix(M)))

print(Math(data=[Matrix(M)]))
print(template.render(matrice=matrice_to_string(M), section2='Short Form'))
geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
# doc = Document(geometry_options=geometry_options)
# doc.append('Etudier la diagonalisabilite de la matrice suivante et donner ses projecteurs spectraux \n')
# doc.append(Math(data=[Matrix(M)]))
# doc.generate_pdf('exo', clean_tex=False)



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
