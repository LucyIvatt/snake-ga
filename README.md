# snake-ga
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)

This repository contains a basic neuroevolution that evolves the weights of a multi-layer perceptron (MLP) using a genetic algorithm. This solution utilises [DEAP](https://deap.readthedocs.io/en/master/), a novel evolutionary computation framework for rapid prototyping and testing of ideas.

## Neural Network Structure
The final algorithm proposed is a conventional neuroevolutionary algorithm (CNE). The
topology of the network is fixed in nature and only the weights of the network are evolved
in the algorithm. 

The network used is a fully-connected multi-layer perceptron with 2
hidden layers. The input layer has 10 nodes that represent local searches for food &
obstacles in the cells immediately above, below, left, and right of the snake, as well as the
direction of the food in the x & y axis

<img width="400" alt="image" src="https://github.com/user-attachments/assets/a4d6eefb-f137-477d-8474-90aea13c0da5">

## Experiments

Before deciding on the final algorithm two different experiments were run to determine the most successful variants of the
algorithm. One experiment looked at different combinations of inputs to the neural network,
and the other looked at modifying the probabilities of crossover and mutation. 

Due to the stochastic nature of genetic algorithms, each algorithm variant was run multiple times and
the statistics averaged. This produced more rigorous results so that reliable and informed
decisions could be made. Each experiment had 2 stages, the exploration stage, and a final
stage. The exploration stage used 5 iterations of each algorithm to explore a wide range of
alterations. The final stage used 15 iterations of each algorithm to analyse the best two
variants found in the exploration stage.

### Neural Network Input Experiment
#### Algorithms Tested

<img width="400" alt="image" src="https://github.com/user-attachments/assets/eefb66c4-6108-43da-807a-4c89915027e4">
<img width="600" alt="image" src="https://github.com/user-attachments/assets/c65842b4-c4df-4875-bd39-fcdd37306015">

#### Results
<img width="400" alt="image" src="https://github.com/user-attachments/assets/1a65a7f6-0128-474e-b2a8-cedd1c60fb38">
<img width="400" alt="image" src="https://github.com/user-attachments/assets/4508c6b2-9c02-4998-aa07-85191453b7e7">

### Crossover & Mutation Probabilities Results

<img width="400" alt="image" src="https://github.com/user-attachments/assets/0e485f6d-765e-4bd9-9913-c0e54221dbf9">
<img width="400" alt="image" src="https://github.com/user-attachments/assets/e8cd087b-c3a1-4ef3-aa0c-6926faa3c57e">

### Final Algorithm
<img width="400" alt="image" src="https://github.com/user-attachments/assets/6daa3250-bf80-4952-b4cf-915bf880b4d5">

_All code submitted as part of the first assessment in the module Evolutionary and Adaptive Computing (EVAC) at the University of York._
