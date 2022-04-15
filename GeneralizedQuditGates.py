#Generalized Qudit Gate Functions
import cirq
import cmath
import numpy as np
from GenQuditGateFunctions import *

w = cmath.exp((2 * 1j * np.pi) / 3)

#SHIFT gate
class GenQuditX(cirq.SingleQubitGate):
	def __init__(self, d, n):
		self.d = d
		self.I_d=np.eye(d)
		self.X_d=np.roll(self.I_d,1,0)
		
	def _qid_shape_(self):
		return(self.d,)
	
	def _unitary_(self):
		return self.X_d
	
	def _circuit_diagram_info_(self, args):
		return '[X]'
		
#QFT Gate
class GenQuditQFT(cirq.SingleQubitGate):
	def __init__(self, d, n):
		self.d = d
		self.n = n
		self.unitary = QFT(d, n)
		
	def _qid_shape_(self):
		return(self.d,)
	
	def _unitary_(self):
		return self.unitary
		
	def _circuit_diagram_info_(self, args):
		return '[QFT]'
		
class GenQuditCShift(cirq.Gate):
	def __init__(self, d, n, index):
		self.d = d
		self.n = n
		self.shape = []
		for x in range(n):
			self.shape.append(d)

		self.unitary = CX_dn(d, n, index)
		self.tuple = tuple(self.shape)
		
	def _qid_shape_(self):
		return self.tuple

	def _unitary_(self):
		return self.unitary

	def _circuit_diagram_info_(self, args):
		return 'o', 'o', '[X]'

class GenF(cirq.Gate):
	def __init__(self, d, n):
		self.d = d
		self.n = n
		self.shape = []
		for x in range(n):
			self.shape.append(d)
			
		self.tuple = tuple(self.shape)
		self.unitary = F_Gate(self.d, self.n)
		
	def _qid_shape_(self):
		return self.tuple		

	def _unitary_(self):
		return self.unitary

	def _circuit_diagram_info_(self, args):
		return 'F'