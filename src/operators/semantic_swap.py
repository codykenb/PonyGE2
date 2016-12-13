from random import randrange
from copy import copy

from algorithm.parameters import params
from representation import individual, tree
from utilities.stats import trackers
from utilities.representation.check_methods import get_output


def semantic_swap(parents):
    """
    Perform semantic swap on a population of individuals. The size of the
    swap population is defined as params['GENERATION_SIZE'] rather than params[
    'POPULATION_SIZE']. This saves on wasted evaluations and prevents search
    from evaluating too many individuals.

    :param parents: A population of parent individuals on which semantic swap
    is to be performed.
    :return: A population of fully semantically swapped individuals.
    """
    
    # Initialise an empty population.
    swap_pop = []
    
    # Iterate over entire parent population
    for ind in parents:
        
        # Make a copy of the individaul so we don't over-write the original
        # parent population.
        ind = ind.deep_copy()
        
        # Semantic swap cannot be performed on invalid individuals.
        if ind.invalid:
            print("Error, invalid ind selected for crossover")
            quit()
        
        # Perform semantic swap on ind.
        ind = semantic_subtree_swap(ind)
        
        if ind.invalid:
            # We have an invalid, need to do swap again.
            pass
        
        elif params['MAX_TREE_DEPTH'] and ind.depth > params['MAX_TREE_DEPTH']:
            # Tree is too deep, need to do swap again.
            pass
        
        elif params['MAX_TREE_NODES'] and ind.nodes > params['MAX_TREE_NODES']:
            # Tree has too many nodes, need to do swap again.
            pass
        
        elif params['MAX_GENOME_LENGTH'] and len(ind.genome) > \
                params['MAX_GENOME_LENGTH']:
            # Genome is too long, need to do swap again.
            pass
        
        else:
            # Swap was successful, extend the new population.
            swap_pop.append(ind)
    
    return swap_pop


def semantic_subtree_swap(ind):
    """
    Given one individual, search the derivation tree to see if any nodes can be
    swapped with existing better nodes from the snippets repository.

    :param ind: Parent 0.
    :return: The new individual.
    """

    # Get the set of labels of non terminals for the tree.
    nodes = ind.tree.get_node_labels_with_output([])

    # Initialise list of possible nodes to swap with existing snippets.
    swap_list = []
    
    for node in nodes:
        # Generate keys to check for snippets.
        key = " ".join([str(node[2].pheno_index), node[0]])
            
        if key in trackers.snippets and not node[2].semantic_lock:
            # We have an existing snippet that we can swap in to improve the
            # current individual.
            swap_list.append([node, trackers.snippets[key], key])
    
    if swap_list:
        # There are improvements to be made

        # Shorten the available swap list by only listing the largest
        # possible tree swaps. Remove trees which are sub-trees of larger
        # trees.
        reduced_swap_list = {}

        for item in swap_list:
            # Find the portion of the phenotype the current tree represents.
            str_section = "".join(item[-1].split()[:2])
            section = eval(str_section)

            # Find the depth of the tree that represents this current section.
            depth = len(str(item[-2]))

            if str_section not in reduced_swap_list:
                # This tree covers a new section of the phenotype, allow it.
                reduced_swap_list[str_section] = [depth, section, item]

            elif depth > reduced_swap_list[str_section][0]:
                # This tree is deeper than the previous entry. We only want
                # the deepest trees to swap in (i.e. we want to lock up the
                # highest possible root nodes).
                reduced_swap_list[str_section] = [depth, section, item]

        # Get the sets of all indices of all subtrees.
        sets = [set(range(reduced_swap_list[item][1][0], reduced_swap_list[
            item][1][1])) for item in sorted(reduced_swap_list)]

        # Remove trees which are sub-trees of larger portions of other trees.
        for item in sorted(reduced_swap_list):
            idx = reduced_swap_list[item][1]
            test_set = set(range(idx[0], idx[1]))
            other_sets = [i for i in sets if i != test_set]

            for each_set in other_sets:
                if test_set.issubset(each_set):
                    # Then the current item in the reduced dictionary is a
                    # subset of an existing item, i.e. the current tree is a
                    # sub-tree of another larger tree in the dictionary.
                    # Remove the current item from the dictionary.
                    reduced_swap_list = {key: value for key, value in
                                         reduced_swap_list.items() if key !=
                                         item}

        # Get the sets of all indices of all subtrees.
        sets = [set(range(reduced_swap_list[item][1][0], reduced_swap_list[
            item][1][1])) for item in sorted(reduced_swap_list)]

        # Remove trees which overlap portions of other trees (not sure if
        # this will work).
        for item in sorted(reduced_swap_list):
            idx = reduced_swap_list[item][1]
            test_set = set(range(idx[0], idx[1]))
            other_sets = [i for i in sets if i != test_set]

            for each_set in other_sets:
                if test_set.intersection(each_set):
                    # Then the current item in the reduced dictionary
                    # intersects with an existing item, i.e. the current tree
                    # overlaps a sub-tree of another tree in the dictionary.
                    # Remove the current item from the dictionary.
                    reduced_swap_list = {key: value for key, value in
                                         reduced_swap_list.items() if key !=
                                         item}

        # Create a list from the reduced dictionary.
        reduced_swap_list = [i[-1] for i in reduced_swap_list.values()]

        # Pick a random item from the reduced swap list.
        for node in reduced_swap_list: # = choice(reduced_swap_list)

            # Make new copy of existing snippet
            new_node = node[1].__copy__()

            # Get parent of original node
            parent = node[0][2].parent

            if parent:
                # Get the index of the original node in the children of its parent.
                idx = parent.children.index(node[0][2])

                # Set new child
                parent.children[idx] = new_node

            # Set parent of new node
            new_node.parent = parent
        
        # Re-map individual with new tree.
        ind = individual.Individual(None, ind.tree)

    return ind


def combine_snippets():
    """
    As the snippets repository grows, we can start to combine
    neighboring snippets to build bigger snippets. Eventually we hope this
    can just build the perfect solution. Iteratively builds snippets until
    no more snippets can be built form the current library.

    :return: Nothing.
    """

    concats = params['BNF_GRAMMAR'].concat_NTs

    # Find the number of snippets at T.
    original_snippets = len(trackers.snippets)

    def concatenate():
        """
        Iterates through all snippets in the snippets dictionary and
        concatenates snippets to make larger snippets.
        
        :return: The new length of the snippets dictionary.
        """
        for snippet in sorted(trackers.snippets.keys()):
            # Find the portion of the phenotype the current tree represents.
            str_section = "".join(snippet.split()[:2])
            section = eval(str_section)
    
            # Find the non-terminal at which the current snippet roots itself.
            NT = snippet.split()[-1]
    
            # Find if this NT exists anywhere in the concatenation NTs
            if NT in concats:
    
                for a_snippet in sorted(trackers.snippets.keys()):
                    # Find the portion of the phenotype the current tree
                    # represents.
                    a_section = eval("".join(a_snippet.split()[:2]))
    
                    # Get the non-terminal of the new snippet.
                    a_NT = a_snippet.split()[-1]
    
                    if a_section[0] == section[1]:
                        # This snippet directly follows on from our current
                        # snippet.
    
                        # Find a concatenation where the a_NT directly follows
                        # the current NT.
                        for i in [concat for concat in concats[NT] if
                                  concat[0][0]['symbol'] == NT and
                                  concat[0][1]['symbol'] == a_NT]:
    
                            # Check to see if the newly concatenated item
                            # already exists in the snippets repository:
                            new_key = " ".join([str([section[0], a_section[1]]),
                                                i[1]])
    
                            if new_key in trackers.snippets:
                                # No need to concatenate as a perfectly good
                                # solution already exists.
                                pass
    
                            else:
                                # We can generate a new snippet by concatenating
                                # two existing snippets.
                                create_snippet(i[1], [trackers.snippets[snippet],
                                                     trackers.snippets[a_snippet]],
                                               i[0], new_key)
    
                    elif a_section[1] == section[0]:
                        # This snippet directly precedes our current snippet.
    
                        # Find a concatenation where the a_NT directly precedes
                        # the current NT.
                        for i in [concat for concat in concats[NT] if
                                  concat[0][1]['symbol'] == NT and
                                  concat[0][0]['symbol'] == a_NT]:
    
                            # Check to see if the newly concatenated item
                            # already exists in the snippets repository:
                            new_key = " ".join([str([a_section[0], section[1]]),
                                                i[1]])
    
                            if new_key in trackers.snippets:
                                # No need to concatenate as a perfectly good
                                # solution already exists.
                                pass
    
                            else:
                                # We can generate a new snippet by concatenating
                                # two existing snippets.
                                create_snippet(i[1], [trackers.snippets[a_snippet],
                                                      trackers.snippets[snippet]],
                                               i[0], new_key)

        return len(trackers.snippets)

    # Perform first pass of concatenation, get the number of snippets at T+1.
    updated_snippets = concatenate()
    
    # Initialise counter for concatenation interations.
    no_passes = 1
    
    print(no_passes, "pass  \tOriginal:", original_snippets,
          "\tNew:", updated_snippets)
    
    while updated_snippets != original_snippets:
        # Keep concatenating snippets until no more concatenations can be made.

        # Save old T+1
        pre_updated_snippets = copy(updated_snippets)

        # Perform concatenation, get the number of snippets at new T+1.
        updated_snippets = concatenate()
        
        # Set new T as old T+1
        original_snippets = pre_updated_snippets
        
        # Increment counter
        no_passes += 1

        print(no_passes, "passes\tOriginal:",
              original_snippets, "\tNew:", updated_snippets)

def create_snippet(parent, children, choice, key):
    """
    Given a parent NT and a list of child trees, create a new tree that acts as
    the parent of the given children. Generates this tree as a snippet and
    adds the new snippet to the trackers.snippets library.

    :param parent: A non-terminal root.
    :param children: A list of derivation tree instances.
    :param choice: The chosen production choice.
    :param key: A new key for the trackers.snippets dictionary.
    :return: Nothing.
    """

    # Initialise new instance of the tree class to act as new snippet.
    new_tree = tree.Tree(parent, None, depth_limit=None)

    # Generate a codon to match the given production choice.
    new_tree.codon = generate_codon(parent, choice)

    # Add the children to the new node
    for child in children:
        new_tree.children.append(child)

        # Set the parent of the child to the new node
        child.parent = new_tree

    # Add new snippet to snippets dictionary
    trackers.snippets[key] = new_tree


def generate_codon(NT, choice):
    """
    Given a list of choices and a choice from that list, generate and return a
    codon which will result in that production choice being made.

    :param NT: A root non-terminal node from which production choices are made.
    :param choice: A production choice from the available choices of the
    given NT.
    :return: A codon that will give that production choice.
    """

    # Find the production choices from the given NT.
    choices = [choice['choice'] for choice in params['BNF_GRAMMAR'].rules[NT][
        'choices']]

    # Find the index of the chosen production and set a matching codon based
    # on that index.
    try:
        prod_index = choices.index(choice)
    except ValueError:
        print("Error: Specified choice", choice, "not a valid choice for "
                                                 "NT", NT)
        quit()

    # Generate a valid codon.
    codon = randrange(len(choices),
                      params['BNF_GRAMMAR'].codon_size,
                      len(choices)) + prod_index

    return codon


def check_snippets_for_solution():
    """
    Check the snippets repository to see if we have built up the correct
    solution yet.
    
    :return: An individual representing the correct solution if it exists,
    otherwise None.
    """

    # Initialise None biggest snippet
    biggest_snippet = [0, None]

    for snippet in sorted(trackers.snippets):
        # Check each snippet to find the largest one.
        if len(get_output(trackers.snippets[snippet])) > biggest_snippet[0]:
            # We have a new biggest snippet.
            biggest_snippet = [len(get_output(trackers.snippets[snippet])),
                               snippet]

    print("Target:       ", params['TARGET'])
    print("Biggest chunk:", get_output(trackers.snippets[biggest_snippet[1]]))
        
    if get_output(trackers.snippets[biggest_snippet[1]]) == params['TARGET']:
        # We have a perfect match
        
        # Generate individual that represents the perfect solution.
        ind = individual.Individual(None, trackers.snippets[biggest_snippet[
            1]])
        
        # Evaluate individual so it will have the perfect fitness.
        ind.evaluate()
        
        # Return ind.
        return ind
    
    else:
        return None
