import pyphen
textFile = open("flesch.txt", "r")
textLines = textFile.readlines()
textString = " ".join(textLines).replace("\n", "")

TotalSentences = len(textString.split("."))
TotalWords = len(textString.split(" "))

dic = pyphen.Pyphen(lang="nl_NL")
WordSplit = textString.split(" ")
TotalSyllables = 0
for s in WordSplit:
    TotalSyllables += len(dic.inserted(s).split("-"))

GradeLevel = 0.39 * (TotalWords / TotalSentences) + 11.8 * (TotalSyllables / TotalWords) - 15.59
print(f"Total Words = {TotalWords}")
print(f"Total Sentences = {TotalSentences}")
print(f"Total Syllables = {TotalSyllables}")
print(f"Grade Level = {GradeLevel}")
