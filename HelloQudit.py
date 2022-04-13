import cirq
import matplotlib.pyplot as plt
import QuditHistogram as quditplt
from QuditGateFunctions import *
from QuditCircuits import *

#Initialize our qudits in 3 dimensions
qudit1 = cirq.LineQid(0, dimension=3)
qudit2 = cirq.LineQid(1, dimension=3)
qudit3 = cirq.LineQid(2, dimension=3)

qudit_array = [qudit1, qudit2, qudit3]

#Initialize circuit
circuitToRun = cirq.Circuit()


##Three Qutrit GGDO##
#Specify number of iterations of Generalized Grover iterator below#
iterations=4
#Define number of runs below#
runs=10000

#Circuit is then constructed below#
circuitToRun.append(grover_init_circuit_3Q(qudit1, qudit2, qudit3))
for i in range(iterations):
	circuitToRun.append(QuditXY_3Q().on(qudit1, qudit2, qudit3))
	circuitToRun.append(grover_diffusion_circuit_3Q(qudit1, qudit2, qudit3))
	#circuitToRun.append(generalized_grover_diffusion_circuit(qudit_array))  
circuitToRun.append(measure_3Q(qudit1,qudit2,qudit3))

##Outputs specified below##
#Print circuit visual
print()
print()
print("---------BEGIN-----------")
print("Circuit:")
print(circuitToRun, end='\n')
print("-------------------------")

#Simulate
simulator = cirq.Simulator()
result = simulator.simulate(circuitToRun)
print(result, end='\n')
print("-------------------------")

##Run simulation set number of times
#Simulation code
result = simulator.run(circuitToRun, repetitions=runs)
#Output run outcomes (commented to prevent clutter)
#print("Results:")
#print(result)
#Output histogram (if possible)
print(quditplt.plot_qudit_state_histogram(result, plt.subplot()))
#Save histogram to external file
histpltfig=quditplt.plot_qudit_state_histogram(result, plt.subplot()).get_figure()
histpltfig.suptitle(str(iterations) + ' Iterations')
histpltfig.savefig('histogram.png')
print("-------------------------")

#Step-by-Step Evolution
print("Step-by-step evolution:")
f = open("stepOutput.txt", "a")
f.write("BEGIN TRIAL\n")
#for i, step in enumerate(simulator.simulate_moment_steps(circuitToRun, qubit_order=[qudit1,qudit2])):      #TWO QUTRIT
for i, step in enumerate(simulator.simulate_moment_steps(circuitToRun, qubit_order=[qudit1,qudit2,qudit3])):#THREE QUTRIT
	print('state at step %d: %s\n' % (i, np.around(step.state_vector(), 2)))
	f.write('state at step %d: %s\n' % (i, np.around(step.state_vector(), 3)))
print("-------------------------\n")
f.write("END TRIAL\n")
f.write("-------------------------\n")
f.close()


#Print resulting unitary
#printUnitary = True
#if printUnitary:
#    print("Resulting Unitary:")
#    print(np.around(cirq.unitary(circuitToRun),3))

#print("----------END------------")
#print()
#print()



#Old Two Qutrit Algr.
#circuitToRun.append(grover_init_circuit_2Q(qudit1, qudit2))
#circuitToRun.append(grover_diffusion_circuit_2Q(qudit1, qudit2, False))
#circuitToRun.append(QuditXY_2Q().on(qudit1, qudit2))
#circuitToRun.append(grover_diffusion_circuit_2Q(qudit1, qudit2, True))