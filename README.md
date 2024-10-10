# snake-ga
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)

This repository contains a basic neuroevolution that evolves the weights of a multi-layer perceptron (MLP) using a genetic algorithm.
https://deap.readthedocs.io/en/master/

## Neural Network Structure
The final algorithm proposed is a conventional neuroevolutionary algorithm (CNE). The
topology of the network is fixed in nature and only the weights of the network are evolved
in the algorithm. The network used is a fully-connected multi-layer perceptron with 2
hidden layers. The input layer has 10 nodes that represent local searches for food &
obstacles in the cells immediately above, below, left, and right of the snake, as well as the
direction of the food in the x & y axis

![thumbnail](https://github.com/user-attachments/assets/babe43b6-a449-4dfa-ba93-aff71015d6c8)

## Individual Representation

![thumbnail (1)](https://github.com/user-attachments/assets/08e7bf06-44a5-4bd1-99bf-06ab36901cb2)

## Experiments

![sensing_function_diagram](https://github.com/user-attachments/assets/937edd13-8640-481a-b6d6-72952a9bb8d0)


### Results

![cx-indpb-exploration-graphs](https://github.com/user-attachments/assets/948358a2-833b-4c6a-8c6f-92137bb31732)
![cx-indpb-final-graphs](https://github.com/user-attachments/assets/5a3790eb-3c19-4144-8032-0fae7b7f5d77)
![final-algorithm-graphs](https://github.com/user-attachments/assets/54b2e745-0a42-42bd-a9c8-ee12955e0d7f)
![input-exploration-graphs](https://github.com/user-attachments/assets/352272f4-5a68-4f3b-a5b7-ef11307a57c7)
![input-final-graphs](https://github.com/user-attachments/assets/4078a2dd-6cd2-4900-b145-4d643087640a)

_All code submitted as part of the first assessment in the module Evolutionary and Adaptive Computing (EVAC) at the University of York._
