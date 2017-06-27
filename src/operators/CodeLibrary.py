# import jsonpickle
import json
import math
from pathlib import Path


class CodeLibrary():
    """
    Curate a library of useful (regex) snippets

    TODO:
    Refactor this class so it is instantiated during initialisation.
    Change json loading to DB persistence layer
    """

    last_best = None

    """
    This is hardcoded for now.
    We may want to maintain a library for each grammar, 
    though we may also want to keep a more general library for a suite of languages
    (e.g. all PCRE-like regex grammars)
    """
    lib_file = "../harvest-lib/regex.json"
    store = []

    def load_existing_material():
        if os.Path.isFile(CodeLibrary.lib_file):
            with open(CodeLibrary.lib_file) as data_file:
                CodeLibrary.store = json.load(lib_file)
        else:
            print("No previous code library found!")

    def harvest_improvement(improved_individual, new_fitness, original_individual):

        # Check if there is actually an improvement worth harvesting
        if math.isnan(new_fitness) or math.isnan(original_individual.fitness):
            return

        if CodeLibrary.last_best == None:
            CodeLibrary.last_best = original_individual

        # check that the fitness has been improved upon
        if CodeLibrary.last_best.fitness < new_fitness:
            return

        # check that the regexes are different
        elif CodeLibrary.last_best.phenotype == improved_individual.phenotype:
            return

        old_material, new_material = CodeLibrary.find_string_diff(
            CodeLibrary.last_best.phenotype, improved_individual.phenotype)

        # can we persist this nicely to a db?
        improvement = {'old_str': old_material,
                       'new_str': new_material,
                       'fit_improvement': (CodeLibrary.last_best.fitness - new_fitness)}
        # In future versions, we could use a diff on the phenotype

        CodeLibrary.add_to_cache(improvement)

        print("Code Library updated, now contains {}".format(
            len(CodeLibrary.store)))

        CodeLibrary.last_best = improved_individual
        CodeLibrary.load_existing_material()
        with open(CodeLibrary.lib_file, 'w+') as outfile:  # create if necessary
            json.dump(CodeLibrary.store, outfile)

    def add_to_cache(improvement):
        found = False
        # See if the improvement exists in the store
        for existing_imp in CodeLibrary.store:
            if existing_imp['old_str'] == improvement['old_str'] and existing_imp['old_str'] == improvement['old_str']:
                found = True
                # update the running average, increment found_count
                existing_imp['fit_improvement'] += (improvement['fit_improvement'] -
                                                    existing_imp['fit_improvement']) / (++existing_imp['found_count'])
                break
        # If this is the first time we are seeing this improvement, save it
        if not found:
            improvement['found_count'] = 1
            CodeLibrary.store.append(improvement)

    def find_string_diff(string_a, string_b):
        """
        Remove the common prefix and suffix from two strings,

        Return the portion of string_a that has been changed,
        and what it was changed to in string_b
        """

        prefix_length = 0
        suffix_length = len(string_a)

        for i in range(len(string_a)):
            if not string_a[i] == string_b[i]:
                prefix_length = i
                break

        for i in range(len(string_a)):
            if not string_a[(len(string_a) - 1) - i] == string_b[(len(string_b) - 1) - i]:
                suffix_length = i
                break
        return string_a[prefix_length:(len(string_a) - suffix_length)], string_b[prefix_length:(len(string_b) - suffix_length)]

    def search_cache(unknown_regex):
        """
        Find relevant transforms likely to improve this new regex.

        Relevant is:

        Likely to improve by 
        performance magnitude
         - when we want to apply these improvements again, we want to test the ones that may have the biggest impact

        improvement frequency
         - when applying again, we want to test the most frequently seen improvement

        """
