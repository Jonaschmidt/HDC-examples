'''
created by Jonas Schmidt on 3/3/2023
'''
from sys import maxsize
import imdb_retriever as imdb
import numpy as np
import hypervector_generation as hgen
import vector_comparison as vcomp

np.set_printoptions(threshold=maxsize)

hypervector_size = 8_000
n_gram_len = 4

train_num = 100
test_num = 50

alphabet = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [],
            'f': [], 'g': [], 'h': [], 'i': [], 'j': [],
            'k': [], 'l': [], 'm': [], 'n': [], 'o': [],
            'p': [], 'q': [], 'r': [], 's': [], 't': [],
            'u': [], 'v': [], 'w': [], 'x': [], 'y': [],
            'z': [], '#': []}
num_seed_vectors = len(alphabet)

# generate hypervectors for symbols
alphabet = hgen.generate_hypervectors(alphabet, hypervector_size)

# get train and test data
train_dict = imdb.get_train(train_num)
test_dict = imdb.get_test(test_num)

# initialize class hypervectors as zero vectors
POS_CLASS = np.zeros(hypervector_size)
NEG_CLASS = np.zeros(hypervector_size)

# train
print("training...")
for sequence in enumerate(train_dict):
    #print(sequence[0])
    sequence = sequence[1]

    # scrub and decompose sequence into n-grams
    seq = hgen.scrub(sequence)
    seq = hgen.decompose_sequence(seq, n_gram_len)

    # encode the n-grams
    for n in enumerate(seq):
        seq[n[0]] = hgen.encode_n_gram(alphabet, n[1])

    # TODO: I believe the bug is here:
    # accumulate the vectors
    acc = np.array(hgen.sum_vec(seq))[0]
    # FIX: acc != np.array(hgen.sum_vec(seq[0]))

    # add accumulated vectors to their respective classes
    if train_dict[sequence] == 0:
        NEG_CLASS = hgen.sum_vec([NEG_CLASS, acc])
    else:
        POS_CLASS = hgen.sum_vec([POS_CLASS, acc])


# test
# binarize classes for testing
POS_CLASS = hgen.binarize(POS_CLASS)
NEG_CLASS = hgen.binarize(NEG_CLASS)

correct = 0

print("testing...")
for sequence in enumerate(test_dict):
    sequence = sequence[1]

    # scrub and decompose sequence into n-grams
    seq = hgen.scrub(sequence)
    seq = hgen.decompose_sequence(seq, n_gram_len)

    # encode the n-grams
    for n in enumerate(seq):
        seq[n[0]] = hgen.encode_n_gram(alphabet, n[1])

    # accumulate the vectors
    acc = np.array(sum(seq))[0]

    # make a prediction
    if(vcomp.cosine_similarity(NEG_CLASS, acc) > vcomp.cosine_similarity(POS_CLASS, acc)):
        prediction = 0
    else:
        prediction = 1

    # if prediction is correct, correct++
    actual = test_dict[sequence]
    if(prediction == actual):
        correct += 1

# output percent correct
print("accuracy (%):", (correct / test_num) * 100)
