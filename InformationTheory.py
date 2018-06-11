import math, random
import collections

from heapq import heappush, heappop, heapify
from collections import defaultdict



#all the possible letters
alphabet = "abcdefghijklmnopqrstuvwxyz "
#The given string
cwmstring = "cwm fjord bank glyphs vext quiz"
twitstring = "twitters tweet twitter"

 
    
def information(thestring):
    #determine how often each letter and space occur
    occurences = {}
    for letter in alphabet:
        occurences[letter] = thestring.count(letter)
        if occurences[letter] == 0:
            del(occurences[letter])
    
    #determine the probability of each letter and space in the string
    prob = {}
    for value in occurences:
        prob[value] = occurences[value]/(1.0*len(thestring))


    #determine the information of each letter and space
    Ixi = {}
    for odd in prob:
        Ixi[odd] = math.log(1.0/prob[odd], 2)

    print("Info", Ixi)

    #determine the Entropy of the string
    H = 0
    for info in Ixi:
        H += Ixi[info]*prob[info]

    print("H is ", H)


    #determine the redundancy of the string
    print("R is ", (math.log(len(thestring),2)-H))
    
    return occurences #for use with twitter part

#The string is special because it contains only one of each of the characters
#so it is nearly not redundant, except for the repeated spaces

def grouping(thestring, size):
    #splits the string into a list
    Groups = []
    listedstring = list(thestring)
    #groups the list into groups of size size
    for index in range(0,len(listedstring), size):
        mygroup = listedstring[index : index + size]
        mygroup = [''.join(mygroup)]
        Groups.append(mygroup)
    single = []
    for pil in Groups:
        single.append(pil[0])
    count = collections.Counter(single)
    return count


def huffman(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    

def restofhuff(seq, occ, huffout):
    print "Symbol\tWeight\tHuffman Code"
    for p in huffout:
        print "%s\t%s\t%s" % (p[0], occ[p[0]], p[1])
    finalencode = []
    for letter in seq:
         finalencode.append(filter(lambda x: letter in x, huffout))
    encode = ""
    print finalencode[-10:]
    for group in finalencode:
        encode = encode + str(group[0][1])
    print "length is", len(encode), "bits"



choice = raw_input("Would you like to use 1 = the cwm string, 2 = the twitter one, 3 = random string, or input your own string?")
numberpergroup = 2
if choice =="3":
    random.seed()
    def random_char(y):
        return ''.join(random.choice(alphabet) for x in range(y))
    
    number = int(raw_input("How many random characters would you like?"))
    seq = random_char(number)

    print("With single characters ")
    out1 = grouping(seq, 1)
    huff1 = huffman(out1)
    restofhuff(seq, out1, huff1)
    
    """for i in range(2, numberpergroup+1):
        out2 = grouping(seq, i)
        seq2 = out2.keys()
        huff2 = huffman(out2)
        
        print "Now with groupings of", i
        restofhuff(seq2, out2, huff2)"""

elif choice == "1":
    information(cwmstring)
    
elif choice == "2":
    out = information(twitstring)
    huff = huffman(out)
    restofhuff(twitstring, out, huff)

else:
    out = information(choice)
    huff = huffman(out)
    restofhuff(choice, out, huff)

