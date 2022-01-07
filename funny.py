import spacy

def numberify(value):
    sum = 0
    result = ""
    addition = ""
    word = value.upper()
    for c in range(len(word)):
        ascii = ord(word[c]) - ord('A') + 1
        sum += ascii
        if (c < len(word) - 1):
            result = f"{result}{word[c]}-"
            addition = f"{addition}{ascii}+"
        else:
            result = f"{result}{word[c]}: "
            addition = f"{addition}{ascii} = {sum}%"
    return [word, sum, f"{result}{addition}"]


nlp = spacy.load("en_core_web_sm")
words = list(nlp.vocab.strings)
data_file = open("funny_output.txt","w+")
hundred_file = open("hundreds.txt","w+")
for value in words:
    if (value.isalpha()):
        result = numberify(value)
        data_file.write(f"{result[2]}\n")
        if (result[1] == 100):
            print(result[2])
            hundred_file.write(f"{result[2]}\n")

