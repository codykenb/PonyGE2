# import jsonpickle
import json
import math

class CodeLibrary():
    """
    Curate a library of useful (regex) snippets
    """

    store=[]
    last_best = None 

    def harvest_improvement(improved_individual, new_fitness, original_individual):

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

        old_material, new_material = CodeLibrary.find_string_diff(CodeLibrary.last_best.phenotype, improved_individual.phenotype)

        # can we persist this nicely to a db?
        improvement = { 'old_str':old_material,
                        'new_str':new_material,
                        'fit_improvement':(CodeLibrary.last_best.fitness - new_fitness) }
        
        CodeLibrary.add_to_cache(improvement)

        print("Code Library updated, now contains {}".format(len(CodeLibrary.store)))
        
        CodeLibrary.last_best = improved_individual

    def add_to_cache(improvement):
        found=False
        for existing_imp in CodeLibrary.store:
            if existing_imp['old_str'] == improvement['old_str'] and existing_imp['old_str'] == improvement['old_str']:
                found=True
                # running average
                existing_imp['fit_improvement'] += ( improvement['fit_improvement'] - existing_imp['fit_improvement'] ) / (++existing_imp['found_count'])
                break
        if not found:
            improvement['found_count']=1
            CodeLibrary.store.append(improvement)

        # TODO: sort the store by the average improvement it has found
        
    def find_string_diff(string_a, string_b):
        prefix_length=0
        suffix_length=len(string_a)

        for i in range(len(string_a)):
            if not string_a[i] == string_b[i]:
                prefix_length = i
                break
            
        for i in range(len(string_a)):
            if not string_a[(len(string_a)-1)-i] == string_b[(len(string_b)-1)-i]:
                suffix_length = i
                break
        return string_a[prefix_length:(len(string_a)-1-suffix_length)], string_b[prefix_length:(len(string_b)-1-suffix_length)]
            
    
