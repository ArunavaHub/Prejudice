import numpy as np
import math
from scipy.linalg import eig

## Ultimatum Game ====================================================================================

def Ultimatum_game(propose, demand):
    if propose>=demand:
        propser=1-propose
        accepter=propose
    else: 
        propser, accepter=0,0
    return propser, accepter

## Payoff for interaction between (Prejudice-Prejudice), (Prejudice-Unprejudice) and (Unprejudice-Unprejudice) =========================

def Payoff(focal_strategy, opponent_strategy, prejudicity, Offer_l):
    focal_strategy_trait,focal_strategy_propose,focal_strategy_demand=focal_strategy[0],float(focal_strategy[1]), float(focal_strategy[2])
    opponent_strategy_trait,opponent_strategy_propose,opponent_strategy_demand=opponent_strategy[0],float(opponent_strategy[1]), float(opponent_strategy[2])
    Accept_l=Offer_l
    if focal_strategy_trait==1 and opponent_strategy_trait==1:
    	if focal_strategy_propose==Offer_l:
    		focal_strategy_propose=focal_strategy_propose+prejudicity
    	if focal_strategy_demand==Accept_h:
    		focal_strategy_demand=focal_strategy_demand-prejudicity
    	if opponent_strategy_propose==Offer_l:
    		opponent_strategy_propose=opponent_strategy_propose+prejudicity
    	if opponent_strategy_demand==Accept_h:
    		opponent_strategy_demand=opponent_strategy_demand-prejudicity
    		

    elif focal_strategy_trait==1 and opponent_strategy_trait==0:
    	if focal_strategy_propose==Offer_h:
    		focal_strategy_propose=focal_strategy_propose-prejudicity
    	if focal_strategy_demand==Accept_l:
    		focal_strategy_demand=focal_strategy_demand+prejudicity

    elif focal_strategy_trait==0 and opponent_strategy_trait==1:
    	if opponent_strategy_propose==Offer_h:
    		opponent_strategy_propose=opponent_strategy_propose-prejudicity
    	if opponent_strategy_demand==Accept_l:
    		opponent_strategy_demand=opponent_strategy_demand+prejudicity
    payoff = Ultimatum_game(focal_strategy_propose,opponent_strategy_demand)[0] + Ultimatum_game(opponent_strategy_propose,focal_strategy_demand)[1]
    return payoff


def Expected_Payoff_Resident(Resident, Mutant, no_of_mutant, Population_Size, prejudicity, Offer_l):

	s=(Population_Size- no_of_mutant-1)*Payoff(Resident, Resident, prejudicity, Offer_l) + no_of_mutant*Payoff(Resident, Mutant, prejudicity, Offer_l)
	return s/(Population_Size-1)


def Expected_Payoff_Mutant(Resident, Mutant, no_of_mutant, Population_Size, prejudicity, Offer_l):

	s=(Population_Size - no_of_mutant)*Payoff(Mutant, Resident, prejudicity, Offer_l) + (no_of_mutant-1)*Payoff(Mutant, Mutant, prejudicity, Offer_l)

	return s/(Population_Size-1)


## Fixation probability =============================================================================================

def Fixation_Prob(Resident, Mutant, Population_Size, prejudicity, Offer_l):

	s=0
	for i in range(1, Population_Size):
		z=1
		for k in range(1, i+1):
			z=z*math.exp(-selection_strength*(Expected_Payoff_Mutant(Resident, Mutant, k, Population_Size, prejudicity,Offer_l)-Expected_Payoff_Resident(Resident, Mutant, k, Population_Size, prejudicity,Offer_l)))
		s+=z
	return 1/(1+s)


def Transition_matrix(strategies, Population_Size, prejudicity, Offer_l):
	mat=np.zeros((len(strategies), len(strategies)))
	for i in range(len(strategies)):
		for j in range(len(strategies)):
			if i!=j:
				mat[i][j]=mutation*Fixation_Prob(strategies[i], strategies[j], Population_Size, prejudicity, Offer_l)
		mat[i][i]=1-sum(mat[i])
	return mat


def main(Offer_l, Population_Size, prejudicity):
	Accept_h=Offer_h
	Accept_l=Offer_l
	strategies=[[1,Offer_h, Accept_h],[1, Offer_h, Accept_l], [1,Offer_l, Accept_h],[1, Offer_l, Accept_l], [0,Offer_h, Accept_h],[0, Offer_h, Accept_l], [0,Offer_l, Accept_h],[0, Offer_l, Accept_l]]
	P=Transition_matrix(strategies, Population_Size, prejudicity, Offer_l)
	eigvals, left_eigvecs = eig(P, left=True, right=False)
	index = np.argmin(np.abs(eigvals - 1))
	left_eigenvector = left_eigvecs[:, index].real
	left_eigenvector /= np.sum(left_eigenvector)
	return left_eigenvector

## Parameter values ============================================================================

Offer_h=Accept_h=0.5
Offer_l=Accept_l=0.1
mutation=10**-3
selection_strength =0.95
prejudicity=0.25
Population_Size=100

## Data generation for frequency of spite over time (Fig3) ======================================================================

strategies=[[1,Offer_h, Accept_h],[1, Offer_h, Accept_l], [1,Offer_l, Accept_h],[1, Offer_l, Accept_l], [0,Offer_h, Accept_h],[0, Offer_h, Accept_l], [0,Offer_l, Accept_h],[0, Offer_l, Accept_l]]
Rho_mat=Transition_matrix(strategies, Population_Size, prejudicity, Offer_l)

generation=10**6
prej_spite_freq=[]
current_freq_dist=[0,0,0,0,1,0,0,0]

for i in range (generation):
	current_freq_dist=np.dot(current_freq_dist, Rho_mat)
	prej_spite_freq.append(current_freq_dist[2]+current_freq_dist[6])

np.savetxt(f'Fig.3/e={prejudicity}_N={Population_size}_w={selection_strength}.txt', prej_spite_freq)


## Data generation for histogram (Fig4) =======================================================================================

result=main(Offer_l, Population_Size, prejudicity)

np.savetxt(f'Fig.4&5(k)/e={prejudicity}_N={Population_size}_w={selection_strength}.txt', result)


