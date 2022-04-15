#Pre-canned Circuits
import cirq
import cmath
import numpy as np
from QuditGateFunctions import *
from GeneralizedQuditGates import *

def grover_diffusion_circuit_2Q(qudit1, qudit2):
	yield QuditQFT().on(qudit1), QuditQFT().on(qudit2)
	yield QuditX().on(qudit1), QuditX().on(qudit2)
	yield QuditQFT().on(qudit2)
	yield QuditCShift_2Q().on(qudit1, qudit2)
	yield QuditI().on(qudit1)
	yield QuditQFTinv().on(qudit2)
	yield QuditXinv().on(qudit1), QuditXinv().on(qudit2)
	yield QuditQFTinv().on(qudit1), QuditQFTinv().on(qudit2)
		
def grover_diffusion_circuit_3Q(qudit1, qudit2, qudit3):
	yield QuditQFT().on(qudit1), QuditQFT().on(qudit2), QuditQFT().on(qudit3)
	yield QuditX().on(qudit1), QuditX().on(qudit2), QuditX().on(qudit3)
	yield QuditQFT().on(qudit3)
	yield QuditCShift_3Q().on(qudit1, qudit2, qudit3)
	yield QuditI().on(qudit1), QuditI().on(qudit2)
	yield QuditQFTinv().on(qudit3)
	yield QuditXinv().on(qudit1), QuditXinv().on(qudit2), QuditXinv().on(qudit3)
	yield QuditQFTinv().on(qudit1), QuditQFTinv().on(qudit2), QuditQFTinv().on(qudit3)
		
def grover_init_circuit_2Q(qudit1, qudit2):
	yield QuditQFT().on(qudit1), QuditQFT().on(qudit2)

def grover_init_circuit_3Q(qudit1, qudit2, qudit3):
	yield QuditQFT().on(qudit1), QuditQFT().on(qudit2), QuditQFT().on(qudit3)

def measure_3Q(qudit1, qudit2, qudit3):
	yield cirq.measure(qudit1, key='q0'), cirq.measure(qudit2, key='q1'), cirq.measure(qudit3, key='q2')

def three_qutrit_gate_test(qudit1, qudit2, qudit3):
	yield QuditCShift_3Q().on(qudit1, qudit2, qudit3)
	yield cirq.measure(qudit1, key='q0'), cirq.measure(qudit2, key='q1'), cirq.measure(qudit3, key='q2')
	
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
	
	yield QuditQFTinv().on(qudit_array[len(qudit_array)-1])
	
	for qudit in qudit_array:
		yield QuditXinv().on(qudit)
		yield QuditQFTinv().on(qudit)

def gen_measure(qudit_array):
	num_q = 0
	for qudit in qudit_array:
		yield cirq.measure(qudit, key="q"+str(num_q))
		num_q = num_q+1