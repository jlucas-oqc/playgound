import numpy as np
import pandas as pd

def qustate(val, n_qubits=1):
    state = np.zeros(2**n_qubits)
    state[val] = 1
    return state

zero_zero = qustate(0,2)
zero_one = qustate(1,2)
one_zero = qustate(2,2)
one_one = qustate(3,2)

cnot = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
cnot_2_1 = np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])

for x in range(4):
    state = qustate(x,2)

    print("cnot")
    print("*")
    print(state)
    print("=")
    print(cnot.dot(state))
    print("="*80)

pauli_x = np.array([[0,1],[1,0]])

for x in range(2):
    state = qustate(x,1)
    print("Pauli_x")
    print("*")
    print(state)
    print("=")
    print(pauli_x.dot(state))
    print("="*80)


