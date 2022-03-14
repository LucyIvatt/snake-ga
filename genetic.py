from game import run_game
from deap import base
from deap import creator
from deap import tools
import logging
import random
import numpy as np
import os
import pickle


def evaluate(individual, network, snake_game, algorithm, display, headless):
    '''Returns the fitness of the individual after evaluating performance from game simulation'''
    network.setWeightsLinear(
        individual)   # Load the individual's weights into the neural network
    # Evaluate the individual by running the game (discuss)
    score = run_game(display, snake_game, headless, network, algorithm)
    return score,


def genetic_algorithm(ind_size, network, snake_game, display, headless, gen_num=150, pop_num=1500, mut_prob=0.021, cx_prob=0.15, exp_type="test", algorithm="b"):
    # Creates single objective maximizing fitness named FitnessMax
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    # Creates an individual with a list of attributes using previously created FitnessMax
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Registers functions to create individuals who's genes are random float values (uniformly distributed between -1 and 1)
    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, -1.0, 1.0)
    toolbox.register("individual", tools.initRepeat,
                     creator.Individual, toolbox.attr_float, n=ind_size)

    # Registers functions to evaluate individuals
    toolbox.register("evaluate", evaluate)

    # Registers function to select, mate and mutate individuals
    toolbox.register("select", tools.selTournament, tournsize=10)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutGaussian,
                     mu=0.0, sigma=0.2, indpb=mut_prob)

    # Registers function to generate initial population
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Registers the statistics & logbook that will be logged during the GA
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("mean", np.mean)
    stats.register("std", np.std)
    stats.register("median", np.median)
    stats.register("min", np.min)
    stats.register("max", np.max)
    logbook = tools.Logbook()

    # Initializes population
    population = toolbox.population(n=pop_num)

    # Calculates the initial fitness values for each individual and sets them
    fitnesses = [toolbox.evaluate(
        individual, network, snake_game, algorithm, display, headless) for individual in population]
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # Genetic Algorithm
    for g in range(gen_num):
        logging.debug("Running generation " + str(g))

        # Selects number of individuals equal to population length
        offspring = toolbox.select(population, len(population))
        # Includes duplicates so clones all individuals
        offspring = list(map(toolbox.clone, offspring))

        # Performs crossover on 2 individuals based on previously defined probability
        for indiv1, indiv2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_prob:
                toolbox.mate(indiv1, indiv2)
                del indiv1.fitness.values
                del indiv2.fitness.values

        # Mutates offspring based on previously defined probability #TODO: Modify probability/algorithm type?
        for mutant in offspring:
            toolbox.mutate(mutant)
            del mutant.fitness.values   # Deletes old fitness values

        # Recalculates fitness values for mutated offspring
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = [toolbox.evaluate(
            individual, network, snake_game, algorithm, display, headless) for individual in invalid_ind]
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Replaces old population with new mutated offspring
        population[:] = offspring

        # Compiles & records the statistics for the new generation
        record = stats.compile(population)
        logbook.record(gen=g, **record)

    save_simulation_info(logbook, population, gen_num,
                         pop_num, mut_prob, cx_prob, exp_type, algorithm)

    return logbook, population


def save_simulation_info(logbook, final_population, gen_num, pop_num, indpb, cx, exp_type, algorithm):
    if exp_type == "final-algorithm":
        root_folder = "sim-outputs//final-algorithm"
    else:
        root_folder = "sim-outputs//" + exp_type + "-experiment"
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    if "cx-indpb" in exp_type:
        parent_folder = root_folder + "//" + "gens-" + str(gen_num) + "-pop-" + str(
            pop_num) + "-mutprob-" + "{:.3f}".format(indpb) + "-cxprob-" + "{:.3f}".format(cx)
    elif "input" in exp_type:
        parent_folder = root_folder + "//" + "gens-" + \
            str(gen_num) + "-pop-" + str(pop_num) + "-algorithm-" + algorithm
    elif exp_type == "final-algorithm":
        parent_folder = root_folder

    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    run_num, folder_made = 1, False
    while not folder_made:
        run_folder = parent_folder + "//run-" + str(run_num)
        if not os.path.exists(run_folder):
            os.makedirs(run_folder)
            folder_made = True
        else:
            run_num += 1

    # Saves label for run
    if not exp_type == "final-algorithm":
        label_file = open(run_folder + "//" + "label" + ".pkl", "wb")

        if "cx-indpb" in exp_type:
            pickle.dump("indpb-" + "{:.3f}".format(indpb) +
                        "-cxprob-" + "{:.3f}".format(cx), label_file)
        elif "input" in exp_type:
            pickle.dump("algorithm-" + algorithm, label_file)

    lb_file = open(run_folder + "//" + "logbook" + ".pkl", "wb")
    pop_file = open(run_folder + "//" + "final_population" + ".pkl", "wb")

    pickle.dump(logbook, lb_file)
    pickle.dump(final_population, pop_file)

    label_file.close()
    lb_file.close()
    pop_file.close()


def load_simulation_info(load_loc):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    output = []
    runs = [load_loc + "//" +
            run for run in os.listdir(load_loc) if os.path.isdir(load_loc + "//" + run)]
    for run in runs:
        label_file = open(run + "//" + "label" + ".pkl", "rb")
        lb_file = open(run + "//" + "logbook" + ".pkl", "rb")
        pop_file = open(run + "//" + "final_population" + ".pkl", "rb")

        output.append((pickle.load(label_file),
                       pickle.load(lb_file),
                       pickle.load(pop_file)))

        label_file.close()
        lb_file.close()
        pop_file.close()
    return output
