from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basicaer import QasmSimulatorPy

circuit = QuantumCircuit(2, 2) #initializing with 2 qubits in the zero state; with 2 classical bits set to zero; and circuit is the quantum circuit.
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])
#QuantumCircuit.h(0): A Hadamard gate 
 #on qubit 0, which puts it into a superposition state.
#QuantumCircuit.cx(0, 1): A controlled-Not operation () on control qubit 0 and target qubit 1, putting the qubits in an entangled state.
#QuantumCircuit.measure([0,1], [0,1]): if you pass the entire quantum and classical registers to measure, the ith qubit’s measurement result will be stored in the ith classical bit.
circuit.draw("mpl") #view the circuit 
#simulate experiment
simulator = AerSimulator()
compiled_circuit = transpile(circuit, simulator)
job = simulator.run(compiled_circuit, shots=1000)
result = job.result()
counts = result.get_counts(circuit)
print("\nTotal count for 00 and 11 are:",counts)
#Visualizing the Results¶
plot_histogram(counts)