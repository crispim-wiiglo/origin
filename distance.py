import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
from math import sqrt 
import timeit

"""
Code for return and plot the minimum distance from a point P(a,b) to a curve f(x) = 620.7x^-0.71

Requisites
----------
numpy, matplotlib and scipy : python3 modules
	install by pip
python3-tk : python3 package
	install by apt
"""

def getDistance(P1, P2):
	"""Returns the distance between point P1 and P2 by Pythagoras.
	
	Parameters
	----------
	P1 : list
		coordinates (x,y) of point P1
	P2 : list 
		coordinates (x,y) of point P2
	"""
	return sqrt((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2)


def fplot():
	"""Plot the graph of f(x) and a circle of radius equal distance and center in point P.
	
	Attributes
	----------
	t : numpy.ndarray
		arrange of values for x from 0 to 100 by steps of 0.1
	"""
	t = np.arange(0.1, 800, 0.1)
	plt.plot(t, f(t))
	plt.plot(np.cos(t) * distance + P[0], np.sin(t) * distance + P[1])
	plt.plot(distance + P[0], distance + P[1],'-')
	plt.plot([P[0]],[P[1]],marker = 'o',markersize = 3, color = 'red')
	plt.plot([xmin],[f(xmin)],marker = 'o',markersize = 3, color = 'blue')
	plt.axis([0, 300, 0, 300])
	plt.grid(True)
	plt.show()

"""
Parameters
----------
a : float
	x coordinate of point P
b : float 
	y coordinate of point P

Lambda Functions
----------------
f : function
	curve f(x)
f1 : function
	the derivative of curve f(x) in x
dist1 : function
	expression of derivative of distance 

Newton
---------
	returns a zero using the Newton-Raphson method

	dist1 : function
		The function whose zero is wanted
	x0 : float
		An initial estimate of the zero
	tol : float, optional
		The allowable error of the zero value
	maxiter : int, optional
		Maximum number of iterations

	xmin: float
		returns estimated location where function is zero
"""

a = float(input("coord x: ")) #mm24h
b = float(input("coord y: ")) #mm1h

P = (a, b)

f = lambda x: 620.7*x**-0.71
f1 = lambda x: -0.71*620.7*x**-1.71
dist1 = lambda x: x - P[0] + f1(x) * (f(x) - P[1])

xmin = newton(dist1, x0 = a, tol=10 ** -10, maxiter=50)
distance = getDistance(P, (xmin, f(xmin)))

print("xmin,fmin: ",xmin,f(xmin))
print("distance: ",distance)

fplot()

