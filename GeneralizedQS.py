import cirq
import matplotlib.pyplot as plt
import QuditHistogram as quditplt
import numpy as np
import cmath
from GenQuditGateFunctions import *
from QuditCircuits import *
from GeneralizedQuditGates import *

##Three Qutrit (Three Valued) Quantum Search##
#This code takes as optional input a max of 
#the range of iterations (always starts at 1)
#and the number of runs for each circuit.
#The simulated results are then outputed as a
#histogram for each number of iterations in the
#form of a png


#Initialize our qudits in 3 dimensions
qudit1 = cirq.LineQid(0, dimension=3)
qudit2 = cirq.LineQid(1, dimension=3)
qudit3 = cirq.LineQid(2, dimension=3)

qudit_array = []


##Three Qutrit GGDO##
##Input dimension of qudits
indim = input("Enter dimension of qudits [default is 3]:")
if indim == '':
    indim = 3
elif type(int(indim)) != int:
    indim = input("Enter dimension of qudits (an integer):")
else:
     indim=int(indim)
##Input number of qudits 
innum = input("Enter number of qudits [default is 3]:")
if innum == '':
    innum = 3
elif type(int(innum)) != int:
    innum = input("Enter number of qudits (an integer):")
else:
     innum=int(innum)
     
for x in range(innum):
    qudit_array.append(cirq.LineQid(x, dimension=indim))

##Input range of iterations 
inpint = input("Enter max of range of iterations [default is 6]:")
if inpint == '':
    iterations = 6
elif type(int(inpint)) != int:
    inpint = input("Enter max of range of iterations (an integer):")
else:
     iterations=int(inpint)
     
#Define number of runs below#
inruns = input("Enter number of runs for each circuit [default is 10,000]:")
if inruns == '':
    runs = 10000
elif type(int(inruns)) != int:
    inruns = input("Enter number of runs for each circuit (an integer):")
else:
    runs = int(inruns)

#Ask if state vector evolution should be output
trackin = input("Track state evolution (y/n)? [default is False]:")
if trackin == ('y' or 'yes' or 'Y' or 'True'):
    track = True
elif trackin == '':
    track = False
else:
    track = False
    print("Didn't catch that, disabling tracking...")

#Set Generalized F gate so it doesn't change
GenF=GenF(indim, innum)

#Print omega values of input vector associated with index and number of each possible entry
diagonal = np.diagonal(GenF.unitary)
stateset = ''
zero = 0
one = 0
two = 0
labels = []
for k in range(indim**innum):
        exponent = round(cmath.log(diagonal[k], w).real)
        if exponent < 0:
            exponent = 3 + exponent
        stateset += ' '+str(k)+':'+str(exponent)
        if exponent == 0:
           zero += 1
        elif exponent == 1:
            one += 1
        elif exponent == 2:
            two += 1
        labels.append(exponent)
stateset=stateset[1:]

print(stateset)
print("Number of ones: "+str(zero))
print("Number of omegas: "+str(one))
print("Number of omega squareds: "+str(two))




#Circuit is then constructed below#
for iteration in range(1,iterations):
    #Initialize circuit
    circuit = cirq.Circuit()
    #Construct circuit
    circuit.append(generalized_grover_init_circuit(qudit_array, indim, innum))
    for i in range(iteration):
	    circuit.append(GenF.on(*qudit_array))
	    circuit.append(generalized_grover_dif_circuit(qudit_array, indim, innum))
    circuit.append(gen_measure(qudit_array))
    #Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=runs)

    #Save histogram to external file
    title='histogram' + str(iteration) + '.png'
    hplt=quditplt.plot_qudit_state_histogram(result, indim, plt.subplot())
    rects = hplt.patches
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        hplt.text(rect.get_x() + rect.get_width() / 2, height+0.01, label,
            ha='center', va='bottom')
    hfig=hplt.get_figure()
    hfig.suptitle(str(iteration) + ' Iterations')
    hfig.savefig("histogram/"+title)
    hfig.clf()
    print("Histogram Saved as " + str(title), end ="\r")
print("Histograms Saved in local histogram folder")



if track == True:
    #Initialize circuit for step evolution
    circuit = cirq.Circuit()
    #Construct circuit
    circuit.append(grover_init_circuit_3Q(qudit1, qudit2, qudit3))
    for i in range(iterations):
        circuit.append(QuditXY_3Q().on(qudit1, qudit2, qudit3))
        circuit.append(grover_diffusion_circuit_3Q(qudit1, qudit2, qudit3))
        #circuitToRun.append(generalized_grover_diffusion_circuit(qudit_array))
    #Simulate
    simulator = cirq.Simulator()

    #Step-by-Step Evolution
    print("Evolution of state vector:")
    f = open("stepOutput.txt", "a")
    f.write("BEGIN TRIAL\n")
    g=1
    for i, step in enumerate(simulator.simulate_moment_steps(circuit, qubit_order=[qudit1,qudit2,qudit3])):#THREE QUTRIT
        if (i % 8 == 0) and (i!= 0):
            print('State after %d Grover iterations:\n %s\n' % (g, np.around(step.state_vector(), 2)))
            g+=1
        f.write('state at step %d: %s\n' % (i, np.around(step.state_vector(), 3)))
            
    print("-------------------------\n")
    f.write("END TRIAL\n")
    f.write("-------------------------\n")
    f.close()
