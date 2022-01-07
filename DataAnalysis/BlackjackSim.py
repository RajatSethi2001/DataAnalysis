def simulate(

def main():
    SplitDict = {}
    AceDict = {}
    RegularDict = {}

    CardList = ['A', '2', '3','4','5','6','7','8','9','T','T','T','T']

    for i in CardList:
        for j in CardList:
            k = str(i) + "," + str(j)
            SplitDict[k] = 'SPLIT'

    for i in range(2, 10):
        for j in CardList:
            k = str(i) + "," + str(j)
            AceDict[k] = 'DOUBLEHIT'

    for i in range(5, 20):
        for j in CardList:
            k = str(i) + "," + str(j)
            RegularDict[k] = 'DOUBLEHIT'


    print(SplitDict)
    print(AceDict)
    print(RegularDict)

main()