import numpy as np
import random

S = np.array([
	[5, 3, 0, 0, 7, 0, 0, 0, 0],
	[6, 0, 0, 1, 9, 5, 0, 0, 0],
	[0, 9, 8, 0, 0, 0, 0, 6, 0],
	[8, 0, 9, 0, 6, 0, 0, 0, 3],
	[4, 0, 0, 8, 5, 3, 0, 0, 1],
	[7, 0, 0, 9, 2, 0, 0, 5, 6],
	[0, 6, 0, 0, 0, 0, 2, 8, 0],
	[0, 0, 0, 4, 1, 9, 0, 3, 5],
	[0, 0, 0, 0, 8, 0, 0, 7, 9]
	]
)

S = np.zeros((9,9))

assert (S.shape == (9,9))

actionSpaces = [[]]*81 #reduce the action space so computing answer is not impossible
for i in range(0, 9):
	for j in range(0, 9):
		if S[i, j] != 0: 
			actionSpaces[i*9+j] = [S[i, j]]
			continue
		a_ij = set(range(1, 10))

		box_i, box_j = 3*(i // 3), 3*(j // 3)
		boxed = set(S[box_i: box_i+3, box_j:box_j+3].flatten())
		if i == 0 and j == 6:
			print(boxed)
			print(S[:, j])
			print(S[i,:])
		a_ij = a_ij.difference(set(S[:, j]).union(set(S[i,:])).union(boxed))
		actionSpaces[i*9+j] = np.array(list(a_ij))


def get_initial_conditions(actionSpaces):
	return [random.choice(Gamma_i) for Gamma_i in actionSpaces]

def get_outcomes(actions):
	actions = np.array(actions).reshape(9, 9)
	outcomes = [None]*81
	for i in range(0, 9):
		for j in range(0, 9):
			J = 0
			gamma_ij = actions[i, j]

			box_i, box_j = 3*(i // 3), 3*(j // 3)

			J = J + (actions[i, :]==gamma_ij).sum() - 1
			J = J + (actions[:, j]==gamma_ij).sum() - 1

			boxed = np.array(actions[box_i: box_i+3, box_j:box_j+3].flatten())
			J = J + (boxed==gamma_ij).sum() - 1
			outcomes[9*i+j] = J
	return outcomes

from itertools import permutations

def improvement_path(actionSpaces, A0): #compute nash equilibrium using improvement path (guaranteed to find one because potential game)
	J = get_outcomes(A0)
	A = A0
	improved = True
	while improved:
		improved = False
		for i in list(np.random.permutation(81)): #one player greedily improves outcome
			actionSpace = set(actionSpaces[i]).difference([A[i]])
			for newAi in list(np.random.permutation(list(actionSpace))):
				oldAi = A[i]
				A[i] = newAi
				newJ = get_outcomes(A)
				if newJ[i] < J[i]:
					J = newJ
					improved = True
				else:
					A[i] = oldAi
	return (A, J)

J = 100
i = 1
while J != 0:
	i = i + 1
	A0 = get_initial_conditions(actionSpaces)
	A, J = improvement_path(actionSpaces, A0)
	if sum(J) == 0: #we only want a nash equilibrium corresponding to the global minimum, J = 0
		print("Solution found! J = ", sum(J)/2)
		print("--------------")
		print(A)
		break
	else:
		print("i: %d -- Bad Nash found: J = %d" %(i, sum(J)/2))



