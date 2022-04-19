#Pre-canned Circuits
import cirq
import cmath
import numpy as np
from GeneralizedQuditGates import *
#GENERALIZED CIRCUITS
def generalized_grover_init_circuit(qudit_array, d, n):
	for qudit in qudit_array:
		yield(GenQuditQFT(d, 1).on(qudit))



def generalized_grover_dif_circuit(qudit_array, d, n):
	for qudit in qudit_array:
		yield GenQuditQFT(d, 1).on(qudit)
		yield GenQuditX(d, 1).on(qudit)
		
	yield GenQuditQFT(d, 1).on(qudit_array[len(qudit_array)-1])
	
	yield GenQuditCShift(d, n, n).on(*qudit_array)
	
	yield QuditQFTinv(d,1).on(qudit_array[len(qudit_array)-1])
	
	for qudit in qudit_array:
		yield QuditXinv(d,1).on(qudit)
		yield QuditQFTinv(d,1).on(qudit)

def gen_measure(qudit_array):
	num_q = 0
	for qudit in qudit_array:
		yield cirq.measure(qudit, key="q"+str(num_q))
		num_q = num_q+1
