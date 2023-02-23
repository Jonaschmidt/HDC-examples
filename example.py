'''
created by Jonas Schmidt on 2/15/2023
'''

print("IMPORTING...")

import imdb_retriever as imdb
print("imdb_retriever IMPORTED")
import hypervector_generation as hgen
print("hypervector_generation IMPORTED")
import vector_comparison as vcomp
print("vector_comparison IMPORTED")

# measure execution time:
from timeit import default_timer as timer
print("timeit IMPORTED")
print("ALL IMPORTS COMPLETED\n")

print("STARTING TIMER...\n")
start = timer()

# hyperparameters
hypervector_size = 10_000
n_gram_len = 3

# alphabet dictionary
# note that '#' character is a default
alphabet = {'a':[],'b':[],'c':[],'d':[],'e':[],
            'f':[],'g':[],'h':[],'i':[],'j':[],
            'k':[],'l':[],'m':[],'n':[],'o':[],
            'p':[],'q':[],'r':[],'s':[],'t':[],
            'u':[],'v':[],'w':[],'x':[],'y':[],
            'z':[],'#':[]}
num_seed_vectors = len(alphabet)

print("ENCODING SYMBOL-SPACE...")
### generating seed hypervectors for atomic elements
alphabet = hgen.generate_hypervectors(alphabet, hypervector_size)
print("SYMBOL-SPACE ENCODED\n")

# print statements...
'''
for letter in alphabet:
    print(letter, ":", alphabet[letter])
'''
# ...

### generating hypervectors for n-grams
# initialize n_grams dictionary as an empty dictionary object
n_grams = {}

# user input for debugging:
'''
sentence = input("Enter a sentence to decompose into n-grams: ").lower()
sentence = hgen.scrub(sentence)
'''
print("SCRUBBING SENTENCE...")
# test input for debugging:
sentence = ("The quick fox jumps over the lazy brown dog").lower()
sentence = hgen.scrub(sentence)
print("SENTENCE SCRUBBED:", sentence, "\n")

n_grams = hgen.decompose_sequence(sentence, n_gram_len)

for n in n_grams:
    n_grams[n] = hgen.encode_n_gram(alphabet, n)

# print statements...
for n in n_grams:
    print(n, ":", n_grams[n])
# ...

# show_vectors demonstration...
'''
vcomp.show_vectors(alphabet, dim_show=100, ones=1)
vcomp.show_vectors(n_grams, dim_show=100, ones=1)
'''
# ...

# other vcomp/vcomp_tf functions demonstration...
print("\nCosine similarity of hypervectors associated with \'a\' and \'b\':", vcomp.cosine_similarity(alphabet['a'], alphabet['b']))
print("Hamming distance of of hypervectors associated with \'a\' and \'b\':", vcomp.hamming_similarity(alphabet['a'], alphabet['b']), "\n")
# ...

train_dict = imdb.get_train(3)
pos_class_hv = []
neg_class_hv = []

print("Positive Class HV:", pos_class_hv)
print("Negative Class HV:", pos_class_hv)

print("TIME ELAPSED:", timer() - start, "s")

