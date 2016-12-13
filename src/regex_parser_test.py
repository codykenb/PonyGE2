import sys
# import ast
# from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, tree
# from antlr4_generated.PCRELexer import PCRELexer
# from antlr4_generated.PCREParser import PCREParser
# # from antlr4_generated.PCREListener import PCREListener
from pprint import pprint
# from random import randrange

from algorithm.parameters import set_params
from operators.semantic_swap import semantic_subtree_swap
#
#
# class PCREPrinter(PCREListener):
#
#     def __init__(self):
#         from algorithm.parameters import params
#         self.grammar = params['BNF_GRAMMAR']
#         self.genome = []
#
#     generated_grammar="<toprule>  ::=  <element>|<recurserule>\n<recurserule>  ::=  <toprule><element>\n<element>  ::=  "
#
#     def enterEveryRule(self, ctx):
#         if len(ctx.children) == 1 and type(ctx.children[0]) is tree.Tree.TerminalNodeImpl :
#             print("Actual  ", repr(ctx.getText()))
#             # prod = ctx.getText()
#             #
#             # for NT in sorted(self.grammar.non_terminals.keys()):
#             #     choices = self.grammar.rules[NT]['choices']
#             #     for choice in choices:
#             #         # print(choice['choice'])
#             #         symbols = [sym['symbol'] for sym in choice['choice']]
#             #         # print("\t", symbols)
#             #         if prod in symbols:
#             #             print("we have found where it lives")
#             #             prod_index = symbols.index(prod)
#             #             codon = randrange(self.grammar.rules[NT]['no_choices'],
#             #                               self.grammar.codon_size,
#             #                               self.grammar.rules[NT]['no_choices']) + prod_index
#             #             print("Codon:", codon)
#             #             self.genome.insert(0, codon)
#             #
#             #             quit()
#             # # quit()
#
#             self.generated_grammar += "\"" + ctx.getText() + "\"|"
#         print("Entering: " + ctx.getText() + " : ")
#         pprint(ctx.children)
#
#     def enterParse(self,ctx):
#         print("Bentering: " + ctx.getText())
#
#     def exitParse(self,ctx):
#         print("Exiting")
#
#
# def main():
#
#     # input = FileStream("a_regex.txt") # "\d.[9-n](\d.).(\w.).(\w.).(\d.).\w\d|y|!|!|Q") #FileStream(argv[1])
#
#     # Bytestring won't work, FileStream/InputStream are from antlr4 library!
# #    input = InputStream("\d.[9-n](\d.).(\w.).(\w.).(\d.).\w\d|y|!|!|Q") #FileStream(argv[1])
#     input = InputStream("\d.[9-n](\d.)")
#
#     lexer = PCRELexer(input)
#     stream = CommonTokenStream(lexer)
#     parser = PCREParser(stream)
#     tree = parser.parse()
#
#
#
#     # quit()
#
#     pony_tree = get_ponyGE2Tree_from_antlrTree(tree)
#
#
# def get_ponyGE2Tree_from_antlrTree(antlr_tree):
#     printer = PCREPrinter()
#     walker = ParseTreeWalker()
#     walker.walk(printer, antlr_tree)
#     print("Done!")
#     print(printer.generated_grammar[:-1])
#     return "yea"
#
        
def test():
    from representation.individual import Individual
    from algorithm.parameters import params
    from utilities.representation.check_methods import print_semantic_lock
    
    genome1 = [43188, 14350, 10956, 4304, 60876, 11863, 65270, 3951, 48513, 15563, 91601, 46390, 10564, 94987, 11320, 98526, 2180, 96063, 41949, 68027, 54015, 54265, 25294, 65328, 96764, 72362, 97409, 43848, 85823, 98763, 22572, 90805, 3951, 48513, 15563, 91601, 46390, 10564, 94987, 91324, 48683, 44137, 98685, 78018, 30143, 15443, 10564, 94987, 72218, 19573, 84621, 4529, 76144, 19921, 8049, 1972, 25366, 84089, 47267, 36384, 93175, 39667, 64848, 41734, 98363, 46390, 10564, 94987, 30385, 93061, 80919, 5242, 59505, 50629, 85146, 83653, 55900, 74687, 72094, 48681, 48545, 25711, 16038, 3026, 69760, 1209, 43169, 25086, 89127, 65248]

    genome2 = [86096, 39592, 57498, 74225, 94841, 33337, 32414, 90613, 27962, 75292, 7179, 88686, 30240, 18185, 29109, 88185, 26295, 1549, 11459, 77753, 9805, 68881, 6857, 32115, 64774, 49351, 65488, 95473, 66039, 50668, 69684, 9123, 89234, 39080, 84751, 63592, 59307, 6719, 47188, 40583, 27962, 75292, 7179, 14322, 68881, 6857, 64501, 1252, 81907, 7024, 99609, 30503, 47868, 74156, 64774, 49351, 65488, 95473, 66039, 50668, 39670, 77474, 94607, 63592, 59307, 61577, 45740, 56245, 54888, 98549, 88232, 54310, 25617, 34180]
    
    genome3 = [77612, 71723, 38913, 33220, 58453, 24105, 8713, 4220, 49143, 6413, 10132, 83915, 29604, 28077, 17887, 84915, 75210, 41580, 8072, 38479, 47891, 72538, 46865, 54337, 80888, 13930, 86788, 74845, 53030, 481, 87173, 60140, 5596, 52464, 51221, 58436, 14725, 18529, 60896, 35417, 8713, 4220, 49143, 73038, 14200, 10027, 79348, 73130, 10132, 83915, 89689, 16660, 87047, 13837, 22793, 2675, 2904, 25436, 32410, 85644, 19183, 62458, 87047, 13837, 22793, 2675, 2904, 94948, 13862, 37087, 10132, 83915, 81041, 46792, 83167, 94296, 78900, 82773, 18529, 60896, 35417, 8713, 4220, 49143, 73038, 14200, 10027, 72770, 83540, 46972, 99360, 29163, 78842, 21318, 20847, 15937]
    
    ind1 = Individual(genome1, None)
    ind2 = Individual(genome2, None)
    ind3 = Individual(genome3, None)
    
    print("Target:     ", params['TARGET'])
    print("Phenotype 1:", ind1.phenotype)
    print("Phenotype 2:", ind2.phenotype)
    print("Phenotype 3:", ind3.phenotype)
    print("")
    
    ind1.evaluate()
    ind2.evaluate()
    ind3.evaluate()
    
    from utilities.stats.trackers import snippets
    
    print(len(snippets), "snippets")
    
    # for snippet in snippets:
    #     print(" ", snippet)
    
    print("")
    
    # print_semantic_lock(ind1.tree)
    # print("")
    # print_semantic_lock(ind2.tree)
    # print("")
    # print_semantic_lock(ind3.tree)
    # print("")

    print("Fitness 1:\t", ind1.fitness)
    print("Fitness 2:\t", ind2.fitness)
    print("Fitness 3:\t", ind3.fitness)
    print("")

    target = "\d.[9-n](\d.).(\w.).(\w.).(\d.).\w\d"
    phen_1 = "[(.\9[n](\d)*).]w.*((\w)(.)\d)(.\w\d)"
    phen_2 = "\d(\9-n\([(.)](\w)*)(\w)(.)\d.*.\w\d"
    phen_3 = "^d.[9-n](\d.).(\w.).++w.1.(\d.).\w\d"

    ind1 = semantic_subtree_swap(ind1)
    ind2 = semantic_subtree_swap(ind2)
    ind3 = semantic_subtree_swap(ind3)

    print("Phenotype 1:", ind1.phenotype)
    print("Phenotype 2:", ind2.phenotype)
    print("Phenotype 3:", ind3.phenotype)
    print("")

    ind1.evaluate()
    ind2.evaluate()
    ind3.evaluate()

    print("")

    print("Fitness 1:\t", ind1.fitness)
    print("Fitness 2:\t", ind2.fitness)
    print("Fitness 3:\t", ind3.fitness)

if __name__ == '__main__':
    set_params(sys.argv)
    test()
