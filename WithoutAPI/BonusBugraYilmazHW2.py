numOfLines=int(input("Number of lines of code of the module: "))
numOfTestCases=int(input("Number of test cases: "))
frequencyOfLinesDict = dict()
costOfTestCasesDict= dict()
testCaseDetailArray=[]
for i in range(numOfTestCases):
  coveredLines=input("Enter the covered lines by test case number #"+str(i+1)+": ")
  coveredLines=coveredLines.split()
  testCaseCost=int(input(("Enter the cost of the test case number #"+str(i+1)+": ")))
  costOfTestCasesDict["T"+str(i+1)]=testCaseCost
  frequencyOfLinesDict["T"+str(i+1)]=len(coveredLines)
  testCaseDetailArray.append(coveredLines)

#calculate efficiency point of each test case
efficiencyPointDict = dict()
for i in range(numOfTestCases):
  efficiencyPointDict[int(i+1)]=0.5*int(costOfTestCasesDict["T"+str(i+1)]) - 0.5*int(frequencyOfLinesDict["T"+str(i+1)])
sortedEfficiencyPoint=sorted(efficiencyPointDict.items(),key=lambda item: item[1])

#Findign the best Test cases to cover all of the lines
linesToBeTested=[]
finalTestCasesDetermined=[]
for i in range(numOfLines):
  linesToBeTested.append(i+1)
testCasesAvailable=[]
for i in range(numOfTestCases):
  testCasesAvailable.append("T"+str(i+1))
while(len(linesToBeTested)!=0):
  for eachLineToBeTested in linesToBeTested:
    for eachEfficientKey in efficiencyPointDict.keys():
      if (str(eachLineToBeTested) in testCaseDetailArray[eachEfficientKey-1])and("T"+str(eachEfficientKey) in testCasesAvailable):
        finalTestCasesDetermined.append("T"+str(eachEfficientKey))
        testCasesAvailable.remove("T"+str(eachEfficientKey))
        for eachLineInTestCase in testCaseDetailArray[eachEfficientKey-1]:
          if(int(eachLineInTestCase) in linesToBeTested):
            linesToBeTested.remove(int(eachLineInTestCase))
        break
print("IDs of the mininmum cost test cases: ",finalTestCasesDetermined)








    


