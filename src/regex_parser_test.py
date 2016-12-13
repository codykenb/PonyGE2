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
    
    genome1 = [51326, 62095, 89625, 47645, 69640, 10488, 17275, 37705, 39670, 37971, 70001, 48800, 77459, 46177, 48195, 3169, 73217, 25692, 65322, 60770, 44157, 80171, 37687, 65295, 8344, 64243, 62095, 89625, 47645, 69640, 6010, 45154, 72035, 12595, 3145, 93473, 24306, 12312, 97583, 51588, 7371, 8250, 45154, 72035, 12595, 3145, 93473, 24306, 33156, 97583, 51588, 63851, 7878, 8344, 64243, 62095, 89625, 47645, 69640, 22350, 97583, 51588, 7371, 61314, 18519, 92693, 35530]

    genome2 = [86096, 39592, 57498, 74225, 94841, 33337, 32414, 90613, 27962, 75292, 7179, 88686, 30240, 18185, 29109, 88185, 26295, 1549, 11459, 77753, 9805, 68881, 6857, 32115, 64774, 49351, 65488, 95473, 66039, 50668, 69684, 9123, 89234, 39080, 84751, 63592, 59307, 6719, 47188, 40583, 27962, 75292, 7179, 14322, 68881, 6857, 64501, 1252, 81907, 7024, 99609, 30503, 47868, 74156, 64774, 49351, 65488, 95473, 66039, 50668, 39670, 77474, 94607, 63592, 59307, 61577, 45740, 56245, 54888, 98549, 88232, 54310, 25617, 34180]
    
    genome3 = [90026, 10957, 35521, 91765, 89971, 36188, 41022, 5094, 62417, 27107, 41977, 47295, 58609, 85466, 456, 64042, 57589, 45833, 68269, 64160, 39325, 32028, 60643, 86740, 65041, 95515, 12299, 61292, 39051, 63122, 69439, 75153, 53060, 28994, 74592, 14155, 50194, 42481, 96533, 6682, 84161, 90585, 74715, 67650, 28994, 36440, 74953, 69565, 42481, 96533, 6682, 84161, 90585, 74715, 43812, 60643, 86740, 65041, 95515, 12299, 61292, 39051, 96316, 28994, 74592, 14155, 57170, 73113, 71629, 19429]
    
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
