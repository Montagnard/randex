#!/usr/bin/env python
import numpy.random as rand
import numpy
import simpy
import math
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, Plot, Figure, Matrix, NoEscape, Command
from pylatex.utils import italic
import os
from latex import build_pdf
from jinja2 import Template, Environment, FileSystemLoader
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

print(os.path.abspath('.'))
template = latex_jinja_env.get_template('jinja-test.tex')


Trigo = [1]*3 + [2]* 2 + [3]*1
Diago = [1]

# Parametres :
shape = Trigo
n = 3
m=200

def rand_cas32(n):
    d = rand.choice([1]*5 + [2]*5 + [3]*4 + [4]*3 + [5]*3 + [0]*7 + [-1]*6 + [-2]*6 + [-3]*2)
    return [[d,1],[d,2]]
def rand_cas33(n):
    d = rand.choice([1]*5 + [2]*5 + [3]*4 + [4]*3 + [5]*3 + [0]*7 + [-1]*6 + [-2]*6 + [-3]*2)
    return [[d,3]]
def rand_cas31(n):
    d = rand.choice([1]*5 + [2]*5 + [3]*4 + [4]*3 + [5]*3 + [0]*7 + [-1]*6 + [-2]*6 + [-3]*2)
    return [[d,1],[d,1], [d,1]]
def rand_cas21(n):
    d1 = rand.choice([1]*5 + [2]*5 + [3]*4 + [0]*7 + [-1]*6 + [-2]*6 + [-3]*2)
    d2 = rand.choice(range(d1+1,10))
    return [[d1,1],[d1,1],[d2,1]]
def rand_cas22(n):
    d1 = rand.choice([1]*5 + [2]*5 + [3]*4 + [0]*7 + [-1]*6 + [-2]*6 + [-3]*2)
    d2 = rand.choice(range(d1+1,10))
    return [[d1,2],[d2,1]]
def rand_cas1(n):
    d1 = rand.choice([1]*5 + [2]*5 + [3]*4 + [0]*7 + [-1]*6 + [-2]*6 + [-3]*2)
    d2 = rand.choice(range(d1+1,10))
    d3 = rand.choice(range(d2+1, 12))
    return [[d1,1],[d2,1],[d3,1]]

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

def roots_to_latex_poly(D) :
    s = "-"
    for d,k in D.items() :
        root = d
        if root == 0:
            mon = "\\lambda"
        elif root > 0 :
            mon = "(\\lambda -" + str(root) + ")"
        else :
            mon = "(\\lambda +" + str(-root) + ")"
        if k == 1:
            exp = ""
        else:
            exp="^"+str(k)
        s = s + mon + exp
    return s

def pol_to_string (pol, X) :
    def mon (i):
        if i == 0:
            return ""
        elif i == 1:
            return X
        else :
            return X + "^" + str (i)
    deg = len(pol)
    s = ""
    for i in range(0, deg) :
        coef = (pol[i].round()).astype(numpy.int64)
        if coef == 0:
            s = s
        elif coef == 1 :
            s = s + "+" + mon(deg - i)
        elif coef == -1 :
            s = s + "-" + mon(deg - i)
        elif coef > 1 :
            s = s + "+" + str(coef) + mon(deg - i)
        else :
            s = s + str(coef) + mon(deg - i)
    return s

class Jordan_form :

    def __init__(self, n) :
        self.block = rand_conf_diag(n)
        blockk = {}
        for (d,k) in self.block:
            try :
                blockk[d] +=1
            except :
                blockk[d] = 1
        blockkk = {}
        for (d,k) in self.block:
            try :
                blockkk[d] +=k
            except :
                blockkk[d] = k
        self.blockk = blockk
        self.blockkk = blockkk
        self.jordan = diag_from_conf(self.block, n)
        l = []
        for x in range(n):
            l.append(self.jordan[x,x])
        self.spectra = l
        self.passage = rand_glZ(n)
        self.inverse = inverse_integer_matrix(self.passage)
        self.matrix = numpy.dot(self.passage, numpy.dot(self.jordan, self.inverse))
        self.poly = numpy.poly(self.jordan)

    def latex_matrix(self) :
        s = latex_matrix(self.matrix)
        return s

    def latex_reduced_form(self) :
        sp = latex_matrix(self.passage)
        sj = latex_matrix(self.jordan)
        spi = latex_matrix(self.inverse)
        s = sp + " \cdot " + sj + " \cdot " + spi
        return s

    def cas(self):
        i = len(self.blockk)
        j = len(self.block)
        if i == 3:
            return "la matrice a trois valeurs propres distinctes et est diagonalisable"
        elif i == 2:
            if j ==3:
                return "la matrice a deux valeurs propres et est diagonalisable"
            else :
                return "la matrice a deux valeurs propre et n'est pas diagonalisable"
        else :
            if j ==3:
                return "la matrice a une seule valeur propre et est diagonalisable"
            if j ==2:
                return "la matrice a une seule valeur propre et n'est pas diagonalisable"
            else :
                return "la matrice a une seule valeur propre et n'est pas diagonalisable"
    def latex_poly(self) :
        pol = -(numpy.poly(self.spectra))
        s = pol_to_string(pol, "\\lambda")
        return s




list_matrix = []
list_sol = []
list_poly = []
for x in range(0,m) :
    M = Jordan_form(n)
    list_matrix.append(M.latex_matrix())
    pol_string = pol_to_string(-(M.poly), "\\lambda")+ "=" + roots_to_latex_poly(M.blockkk)
    s = "Le polynome caracteristique de la matrice est donne par $$" + pol_string + "$$"
    for (d, k) in M.blockk.items() :
        N = M.matrix-d*numpy.identity(n).astype(int)
        s = s + "$$M - " + str(d) + "Id =" + latex_matrix(N)
        s = s +"$$ Et on a $"
        s = s + "dim(E_{"+ str(d)+"}) =" + str(k) + "$."
    s = s.replace("- -", "+")
    s = s + "\\ On est donc dans le cas où " + M.cas() +  ". On peut ecrire par exemple la matrice sous la forme :"
    s = s + "$$"+ M.latex_reduced_form() + "$$"
    list_sol.append(s)


D = {}
D["list_matrix"] = list_matrix
D["list_sol"] = list_sol
D["list_poly"] = list_poly
tex = template.render(D)
f= open("result.tex","w+")
f.write(tex)
f.close() 
pdf = build_pdf(tex)
pdf.save_to('ex1.pdf')


# doc = Document(geometry_options=geometry_options)
# doc.append(Math(data=[Matrix(M)]))
# doc.append('Le polynome caracteristique est donnee par :')

# doc.append(Math(data=[NoEscape(d)]))
#
# doc.append(Math(data=[NoEscape('2\\frac{3}{2}'),"_", 8]))
#
# doc.generate_pdf('corrige', clean_tex=False)
