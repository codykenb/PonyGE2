from fitness.evaluation import evaluate_fitness
from operators.crossover import crossover
from operators.mutation import mutation
from operators.replacement import replacement
from operators.selection import selection
from operators.semantic_swap import semantic_swap, combine_snippets
from utilities.stats import trackers
from utilities.representation.check_methods import get_output


def step(individuals):
    """
    Runs a single generation of the evolutionary algorithm process:
        Selection
        Variation
        Evaluation
        Replacement
    
    :param individuals: The current generation, upon which a single
    evolutionary generation will be imposed.
    :return: The next generation of the population.
    """

    # Select parents from the original population.
    parents = selection(individuals)

    # Crossover parents and add to the new population.
    cross_pop = crossover(parents)

    # Mutate the new population.
    new_pop = mutation(cross_pop)

    # Evaluate the fitness of the new population.
    new_pop = evaluate_fitness(new_pop)

    # Replace the old population with the new population.
    individuals = replacement(new_pop, individuals)
    
    return individuals


def semantic_step(individuals):
    """
    Runs a single generation of the evolutionary algorithm process:
        Selection
        Variation
        Evaluation
        Replacement

    :param individuals: The current generation, upon which a single
    evolutionary generation will be imposed.
    :return: The next generation of the population.
    """
    
    # Select parents from the original population.
    parents = selection(individuals)
    
    # Perform semantic swap on parents.
    swap_pop = semantic_swap(parents)

    # Evaluate the fitness of the new population.
    eval_pop = evaluate_fitness(swap_pop)
    
    # Mutate the new population.
    new_pop = mutation(eval_pop)
    
    # Evaluate the fitness of the new population.
    new_pop = evaluate_fitness(new_pop)
    
    # Replace the old population with the new population.
    individuals = replacement(new_pop, individuals)

    # biggest_snippet = [0, None]
    # print(len(trackers.snippets))
    # for snippet in sorted(trackers.snippets):
    #     if len(get_output(trackers.snippets[snippet])) > biggest_snippet[0]:
    #         biggest_snippet = [len(get_output(trackers.snippets[snippet])), snippet]
    #
    # print("\nLargest snippet:", get_output(trackers.snippets[biggest_snippet[
    #     1]]))#, "\n", str(trackers.snippets[biggest_snippet[1]]))

    # Combine snippets to make bigger snippets. Quickly builds up the
    # perfect solution.
    combine_snippets()

    return individuals
