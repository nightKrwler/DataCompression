class Lz77:
    def __init__(self, sliding_window_size, search_buffer_size):
        self.sws = sliding_window_size
        self.sbs = search_buffer_size
        self.encoded_text = ""
        self.codes = []
    
    def compressor(self,data):
        encoded_text  = ""
        position = 0 
        offset = 0
        max_match_length = 0
        while(position<len(data)):
            #print("a")
            offset,max_match_length,codeword =  self.match(position,data)
            self.codes.append([offset,max_match_length,codeword])
            position += max_match_length+1
            #print("c", max_match_length)
            encoded_text = encoded_text+str(offset)+" "+ str(max_match_length)+" "+codeword+" "
        self.encoded_text = encoded_text
        return encoded_text

    def match(self, position, data):
        sb = self.sbs
        i = 1
        key = data[position]
        max_match_length = 0
        offset = 0
        while((position-i)>=0 and i!=sb+1):
            #print("b")
            length = 0
            if(data[position-i]==key):
                length+=1
                j = 1
                while(position-i+j!= len(data)):
                    if(data[position-i+j]== data[position+j]):
                        length+=1
                        j+=1
                    else:
                        break
                if(max_match_length<length):
                    max_match_length = length
                    offset = i
            i +=1
        return offset,max_match_length,data[position+max_match_length]

    def decompressor(self):
        decoded_text = ""
        for code in (self.codes):
            pointer_position = len(decoded_text)
            offset = code[0]
            length = code[1]
            code_word = code[2]
            for j in range(length):
                decoded_text += decoded_text[pointer_position-offset+j] 
            decoded_text+=code_word

        return decoded_text


path = "./data.txt"
outpath = "./lz77_compressed.txt"
outpath2 = "./lz77_decompressed.txt"
file1 = open(path,'r')
data = file1.read()
sliding_window_size = 13
search_buffer_size = 7
lz = Lz77(sliding_window_size, search_buffer_size)
compressed = lz.compressor(data)
output_compressed = open(outpath,'w')
output_decompressed = open(outpath,'w')

output_compressed.write(compressed)

decompressed  = lz.decompressor()
output_decompressed.write(decompressed)
