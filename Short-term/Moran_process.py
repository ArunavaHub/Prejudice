import numpy as np
import random
from numba import jit,njit,prange

## Ultimatum Game ====================================================================================

@njit
def Ultimatum_game(propose, demand):
    if propose>=demand:
        propser=1-propose
        accepter=propose
    else: 
        propser, accepter=0,0
    return propser, accepter


## Payoff for interaction between (Prejudice-Prejudice), (Prejudice-Unprejudice) and (Unprejudice-Unprejudice) =========================

@njit
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


## Construction of payoff matrix ===========================================================
@njit
def Payoff_mat(Strategies, prejudicity, Offer_l):
	payoff_mat=np.zeros((len(Strategies), len(Strategies)))
	for i in range (len(Strategies)):
		for j in range(len(Strategies)):
			focal_strategy=Strategies[i]
			opponent_strategy=Strategies[j]
			payoff_mat[i][j]=Payoff(focal_strategy, opponent_strategy, prejudicity, Offer_l)
	return payoff_mat


## Finding the fitnesses of strategies =======================================================
@njit
def Fitness(Strategies, Payoff_matrix, Count_Strategies):
	No_of_strategies=len(Strategies)
	Fitness_strategies=np.zeros(No_of_strategies)
	for i in range(No_of_strategies):
		Count_Strategies[i]=Count_Strategies[i]-1
		tems=Count_Strategies.astype(np.float64)
		Fitness=(np.dot(Payoff_matrix, tems)/(sum(Count_Strategies)))
		Fitness_strategies[i]=1-selection_strength+selection_strength*Fitness[i]		
		Count_Strategies[i]=Count_Strategies[i]+1
	return Fitness_strategies


## Birth process===============================================================================
@njit
def Birth_strategy(Distribution_Pick, Count_Strategies):
	x1=np.random.uniform(0,1)
	for i in range(len(Count_Strategies)):
		if Distribution_Pick[i]<x1<=Distribution_Pick[i+1]:
			Count_Strategies[i]=Count_Strategies[i]+1
	return Count_Strategies

## Death Process ===============================================================================
@njit
def Death_strategy(Distribution_replacement, Count_Strategies):
	x2=np.random.uniform(0,1)
	for i in range(len(Count_Strategies)):
		if Distribution_replacement[i]<x2<=Distribution_replacement[i+1]:
			Count_Strategies[i]=Count_Strategies[i]-1
	return Count_Strategies

## Moran Process =================================================================================
@njit
def Moran_process(Strategies, Count_Strategies, Fitness_strategies):

	No_of_strategies=len(Strategies)
	Freq_Strategies=Count_Strategies/sum(Count_Strategies)
	tems=Count_Strategies.astype(np.float64)
	Total_fitness=np.dot(tems, Fitness_strategies)
	Relative_fitness=Fitness_strategies/Total_fitness
	Prob_pick=np.zeros(No_of_strategies)
	Prob_replacement=np.zeros(No_of_strategies)
	Distribution_Pick=np.zeros(No_of_strategies+1)
	Distribution_replacement=np.zeros(No_of_strategies+1)

	for i in range(No_of_strategies):
		Prob_pick[i]=Count_Strategies[i]*Relative_fitness[i]
		Prob_replacement[i]=Freq_Strategies[i]
		Distribution_Pick[i+1]=Distribution_Pick[i]+Prob_pick[i]
		Distribution_replacement[i+1]=Distribution_replacement[i]+Prob_replacement[i]

	x1=np.random.uniform(0,1)
	if x1<=Mutation_rate:
		strat_array=np.arange(0, len(Strategies), 1)
		random_selected_strategy=np.random.choice(strat_array)
		Count_Strategies[int(random_selected_strategy)]+=1
	else:
		Count_Strategies=Birth_strategy(Distribution_Pick, Count_Strategies)
	Count_Strategies=Death_strategy(Distribution_replacement, Count_Strategies)

	return Count_Strategies


## Making a Population =================================================================================
@njit
def Population(Population_size, Strategies):

	Population_array=[0]*Population_size
	strat_array=np.arange(0, len(Strategies), 1)
	Count_Strategies=[]
	for i in range(Population_size):
		Population_array[i]=np.random.choice(strat_array)
	for i in range(len(Strategies)):
		Count_Strategies.append(Population_array.count(strat_array[i]))
	return Count_Strategies


## Freqency of strategies over prejudice ==============================================================================================

@njit
def Freq_vs_Prejudice(prejudicity, Offer_l):
	Accept_l=Offer_l
	Strategies=np.array([[1,Offer_h, Accept_h],[1, Offer_h, Accept_l], [1,Offer_l, Accept_h],[1, Offer_l, Accept_l],
            [0,Offer_h, Accept_h],[0, Offer_h, Accept_l], [0,Offer_l, Accept_h],[0, Offer_l, Accept_l]])
	No_of_strategies = len(Strategies)
	Count_Strategies=np.array(Population(Population_size, Strategies))
	Average_freq = np.zeros(No_of_strategies)
	payoff_matrix=Payoff_mat(Strategies, prejudicity, Offer_l)
	for i in range (No_of_generation):
		Fitness_strategies=Fitness(Strategies, payoff_matrix, Count_Strategies)
		Count_Strategies=Moran_process(Strategies, Count_Strategies, Fitness_strategies)
		Freq_over_generation = Count_Strategies/Population_size
		Average_freq = (i*Average_freq+Freq_over_generation)/(i+1)
		# print(i)
	return Average_freq


No_of_generation=10**8
time=np.arange(0,No_of_generation, 1)


## Data generation for Bar diagram =====================================================================================================================

prejudicity=0.25
Mutation_rate = 0.05
selection_strength= 0.5
Population_size= 100

Average_freq=Freq_vs_Prejudice(prejudicity)

np.savetxt(f'Fig.1&5(a-i)/e={prejudicity}_N={Population_size}_w={selection_strength}.txt', Average_freq)
##=======================================================================================================================================================

## Data generation for frequnecy over prejudice =========================================================================================================

Offer_h=Accept_h=0.5
Offer_l=Accept_l=0.1
Mutation_rate = 0.05
selection_strength= 0.5
Population_size= 100
prejudice_array=np.linspace(0, Offer_h- Offer_l, 51)

@njit(parallel=True)
def parallel_code(prejudice_array):
	Data=np.zeros((len(prejudice_array),len(Strategies)))
	for i in prange(len(prejudice_array)):
		# print(i)
		Data[i]=Freq_vs_Prejudice(prejudice_array[i])
	return Data

Data=parallel_code(prejudice_array)

np.savetxt(f'Fig.2/N={Population_size}_w={selection_strength}.txt', Data)
##=======================================================================================================================================================


## Data generation for contour plot =====================================================================================================================

Offer_h=Accept_h=0.5
Mutation_rate = 0.05
selection_strength= 0.5
Population_size= 100

@njit
def main(input_data):
	prejudicity=input_data[0]
	Offer_l=input_data[1]
	Accept_l=Offer_l
	Strategies=np.array([[1,Offer_h, Accept_h],[1, Offer_h, Accept_l], [1,Offer_l, Accept_h],[1, Offer_l, Accept_l],
            [0,Offer_h, Accept_h],[0, Offer_h, Accept_l], [0,Offer_l, Accept_h],[0, Offer_l, Accept_l]])

	if Offer_l+prejudicity<=Offer_h:
		freq=Freq_vs_Prejudice(prejudicity, Offer_l)
	else:
		freq=np.ones(len(Strategies))
	return freq

Offer_l_array=np.linspace(0.0, 0.5, 51)
prejudicity_array=np.linspace(0,0.5, 51)
input_array=[]
for i in range(len(prejudicity_array)):
	for k in range(len(Offer_l_array)):
		input_array.append([prejudicity_array[i], Offer_l_array[k]])

input_array=np.array(input_array)
@njit(parallel=True)
def parallel_code(input_array):
	Data=np.zeros((len(input_array),8))
	for i in prange(len(input_array)):
		Data[i]=main(input_array[i])
	return Data

Data=parallel_code(input_array)

np.savetxt(f'Fig.6/N={Population_size}_w={selection_strength}.txt', Data)
##=======================================================================================================================================================


