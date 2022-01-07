DensityDataFile = open("DensityData.csv", "r", encoding="utf-8-sig")
DensityData = DensityDataFile.readlines()
DensityDataDict = {}

DensityData[0] = DensityData[0].split(",")
INDEX_DEN_2015 = DensityData[0].index("2015")
INDEX_DEN_2018 = DensityData[0].index("2018")


GDPDataFile = open("GDPData.csv", "r", encoding="utf-8-sig")
GDPData = GDPDataFile.readlines()
GDPDataDict = {}
GDPChangeDict = {}

GDPData[0] = GDPData[0].split(",")
INDEX_GDP_2015 = GDPData[0].index("2015")
INDEX_GDP_2018 = GDPData[0].index("2018")


RegDataFile = open("RegData.csv", "r", encoding="utf-8-sig")
RegData = RegDataFile.readlines()
RegDataDict = {}

RegData[0] = RegData[0].split(",")
INDEX_REG_2015 = RegData[0].index("2015")
INDEX_REG_2018 = RegData[0].index("2018")

DEN_WEIGHT = 0.05
GDP_WEIGHT = -0.35
GDP_CHANGE_WEIGHT = 0.4
REG_WEIGHT = 0.20

CountrySet = set()
CompositeData = []
WeightData = []

for i in range(1, len(DensityData)):
    DensityData[i] = DensityData[i].replace('"', '').split(",")
    if (DensityData[i][INDEX_DEN_2015] != '' and DensityData[i][INDEX_DEN_2018] != ''):
        DensityDataDict[DensityData[i][0]] = float(DensityData[i][INDEX_DEN_2018]) / float(DensityData[i][INDEX_DEN_2015])

for i in range(1, len(GDPData)):
    GDPData[i] = GDPData[i].replace('"', '').split(",")
    if (GDPData[i][INDEX_GDP_2015] != '' and GDPData[i][INDEX_GDP_2018] != ''):
        GDPDataDict[GDPData[i][0]] = float(GDPData[i][INDEX_GDP_2018])
        GDPChangeDict[GDPData[i][0]] = float(GDPData[i][INDEX_GDP_2018]) / float(GDPData[i][INDEX_GDP_2015])

for i in range(2, len(RegData)):
    RegData[i] = RegData[i].replace('"', '').split(",")
    if (RegData[i][INDEX_REG_2018] != '#N/A'):
        RegDataDict[RegData[i][0]] = float(RegData[i][INDEX_REG_2018])

#print("Density Data ======================================= ")
for i in DensityDataDict.keys():
    if (i in GDPDataDict and i in RegDataDict):
        CountrySet.add(i)

"""
    else:
        print(i)

print("GDP Data =========================================== ")
for i in GDPDataDict.keys():
    if not(i in CountrySet):
        print(i)

print("Reg Data =========================================== ")
for i in RegDataDict.keys():
    if not(i in CountrySet):
        print(i)
"""

WeightData = ["", DEN_WEIGHT, GDP_WEIGHT, GDP_CHANGE_WEIGHT, REG_WEIGHT]
for i in CountrySet:
    CompositeData.append([i, DensityDataDict[i], GDPDataDict[i], GDPChangeDict[i], RegDataDict[i]])

for c in range(1, len(CompositeData[0])):
    CompositeData.sort(key=lambda x: x[c])
    MaxValue = CompositeData[len(CompositeData)-1][c]
    for r in range(len(CompositeData)):
        CompositeData[r][c] = round(CompositeData[r][c] * WeightData[c] / MaxValue, 4)

for r in range(len(CompositeData)):
    sum = 0
    for c in range(1, len(WeightData)):
        sum += CompositeData[r][c]
    CompositeData[r].append(round(sum, 4))

CompositeData.sort(key=lambda x: x[len(CompositeData)-1])
CompositeData.reverse()
for r in CompositeData:
    print(r)
    
DensityDataFile.close()
GDPDataFile.close()
RegDataFile.close()
