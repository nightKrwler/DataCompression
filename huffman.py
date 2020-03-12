import heapq
import pandas as pd 
import numpy as np 
from collections import Counter
import re
from functools import total_ordering

@total_ordering
class Node:
    def __init__(self, freq,char):
        self.left = None
        self.right= None
        self.fre = freq
        self.key = char
    
    # defining comparators less_than and equals
    def __lt__(self, other):
        return self.fre < other.fre

    def __eq__(self,other):
        if(other == None):
            return False
        if(not isinstance(other , Node)):
            return False
        return self.fre == other.fre

class Tree:
    def __init__(self,listfreq):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        for key in listfreq:
            node = Node(listfreq[key], key)
            heapq.heappush(self.heap,node)

        while(len(self.heap)>1):
            t1 = heapq.heappop(self.heap)
            t2 = heapq.heappop(self.heap)
            count = t1.fre + t2.fre
            D = Node(count,None)
            D.left = t1
            D.right = t2
            heapq.heappush(self.heap, D)
		
    
    def huffmancode(self, root, current_code):
        if (root == None) :
            return

        if(root.key != None):
            self.codes[root.key] = current_code
            self.reverse_mapping[current_code] = root.key
            return
        
        self.huffmancode(root.left,current_code+"0")
        self.huffmancode(root.right, current_code+"1")

    def compress(self, text):
        encoded_text =  "".join(self.codes[let] for let in text)
        extra_padding = 8 - len(encoded_text)%8
        for i in range(extra_padding):
            encoded_text += "0"
        
        padded_count = "{0:08b}".format(extra_padding)

        padded_encoded_text = padded_count + encoded_text

        if(len(padded_encoded_text)%8 !=0):
            print(" NOt padded properly")
            exit(0)

        b = bytearray()

        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte,2))
        
        output_path = "compressed.bin"
        output = open(output_path, 'wb')

        output.write(bytes(b))

        print("Compressed Successfully")
        return output_path

    def decompress(self, input_path):

        output_path = "decompressed.txt"
        output = open(output_path, 'w')
        bit_string = ""
        file = open(input_path,'rb')
        byte = file.read(1)

        while(len(byte)!=0):
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8,'0')
            bit_string += bits
            byte = file.read(1)

        padded_count = bit_string[:8]
        extra_padding = int(padded_count,2)
        bit_string = bit_string[8:]
        encoded_text = bit_string[:-1*extra_padding]
        current_Code = ""
        decoded_txt = ""
        for bit in encoded_text:
            current_Code +=bit
            if(current_Code in self.reverse_mapping):
                character = self.reverse_mapping[current_Code]
                decoded_txt += character
                current_Code = ""
        
        output.write(decoded_txt)
        print("Decompressed succesfully")
        return output_path


def main():

    path = "./data.txt"
    file1 = open(path,'r')
    data = file1.read()
    res = Counter(data)
    tree =  Tree(res)
    root = heapq.heappop(tree.heap)
    s = ''
    tree.huffmancode(root,s)
    #print(tree.codes)
    compressed_path = tree.compress(data)
    decompressed_path = tree.decompress(compressed_path)

if __name__ == "__main__":
    main()