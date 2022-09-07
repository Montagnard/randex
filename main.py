#!/usr/bin/env python
import numpy.random as rand
import numpy
import simpy
import math
from pylatex import Matrix
import os
from latex import build_pdf
from jinja2 import Template, Environment, FileSystemLoader

Trigo = [1]*3 + [2]* 2 + [3]*1
Diago = [1]

# Parametres :
shape = Trigo
# Dimension de la matrice (pour l'instant 3)
n = 3
n_exo = 10

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
            s = s + "+" + mon(deg - i - 1)
        elif coef == -1 :
            s = s + "-" + mon(deg - i - 1)
        elif coef > 1 :
            s = s + "+" + str(coef) + mon(deg - i - 1)
        else :
            s = s + str(coef) + mon(deg - i - 1)
    return s

def add_latex(n):
    return ("+ " + str(n)).replace("+ -", "- ")

class Jordan_form :

    def __init__(self, n) :
        self.dim = n
        self.jordan_blocks= rand_conf_diag(n)
        self.mult_geo = {}
        for (d,k) in self.jordan_blocks:
            try :
                self.mult_geo[d] +=1
            except :
                self.mult_geo[d] = 1
        self.mult_alg = {}
        for (d,k) in self.jordan_blocks:
            try :
                self.mult_alg[d] +=k
            except :
                self.mult_alg[d] = k
        self.jordan = diag_from_conf(self.jordan_blocks, n)
        self.spectra = [ self.jordan[x,x] for x in range(n)]
        self.passage = rand_glZ(n)
        self.inverse = inverse_integer_matrix(self.passage)
        self.matrix = numpy.dot(self.passage, numpy.dot(self.jordan, self.inverse))
        self.poly = numpy.poly(self.jordan)
        self.is_diago = (self.mult_geo == self.mult_alg)

    def poly_factored_latex(self, x) :
        s = "-"
        for d,k in self.mult_alg.items() :
            root = d
            if root == 0:
                mon = x
            elif root > 0 :
                mon = "(" + x + " -" + str(root) + ")"
            else :
                mon = "(" + x + " +" + str(-root) + ")"
            if k == 1:
                exp = ""
            else:
                exp="^"+str(k)
            s = s + mon + exp
        return s

    def latex_poly(self, x) :
        pol = -(numpy.poly(self.spectra))
        s = pol_to_string(pol, x)
        return s

    def shifted_matrix(self, x):
        N = self.matrix-x*numpy.identity(self.dim).astype(int)
        return N

    def basis_eigenspace(self, root):
        l = []
        i = 0
        for (d,k) in self.jordan_blocks:
            if d == root :
                vect = self.passage.T[i]
                s = "\\\\".join([ str(x) for x in vect])
                l.append(s)
            i += k
        return l


list_matrix = []
list_sol = []
list_poly = []
for x in range(0,n_exo) :
    M = Jordan_form(n)
    list_matrix.append(M)

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

D = {}
D["list_matrix"] = list_matrix
D["n_exo"] = n_exo
D["latex_matrix"] = latex_matrix
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
