import cplex

#generates 2D array that stores which lines of code is tested by witch test case
def generateTwoDimArray():  
  numOfLines=int(input("Enter The Number Of Lines in The Module: "))
  numOfTestCases=int(input("Enter The Number Of Test Cases: "))
  # lineTestCasesArray[numOfTestCases+1][numOfLines]
  w,h=numOfLines,numOfTestCases+1
  lineTestCasesArray=[[0 for x in range(w)] for y in range(h)] 
  for i in range(numOfTestCases+1): #Giving Line names and filling the array with -1
    for j in range(numOfLines):
      if(i==0):
        lineTestCasesArray[i][j]="Line" + " " +  str(j+1)
      else:
        lineTestCasesArray[i][j]=-1
  for i in range(numOfTestCases): #Filling the array based on the user input (Putting Test cases Under the line numbers)
    coveredLines=input("Enter The Covered Lines By Test Case Number #"+str(i+1)+": ")
    coveredLines=coveredLines.split()
    for eachLineCovered in coveredLines:
      eachLineCovered = int(eachLineCovered)
      for j in range(numOfTestCases):
        if(lineTestCasesArray[j+1][eachLineCovered-1]==-1):  #find first empty slot on the vertical column of the line
          lineTestCasesArray[j+1][eachLineCovered-1] ="T"+str(i+1)  #insert the test case in the first empty vertical slot
          break
  return lineTestCasesArray

#solves the ILP problem by using cplex Api
def solveILP(ilpArray):
  cplexObject=cplex.Cplex()
  numOfTestCases=len(ilpArray)-1
  objective=[]
  lowerBounds=[]
  upperBounds=[]
  varNames=[]
  varTypes=[]
  for i in range(numOfTestCases):
    objective.append(1)
    lowerBounds.append(0)
    upperBounds.append(1)
    varNames.append("T"+str(i+1))
    varTypes.append("B") # Binary Variables
  cplexObject.variables.add(obj=objective,lb=lowerBounds,ub= upperBounds,names= varNames)
  cplexObject.objective.set_sense(cplexObject.objective.sense.minimize) #Specifying it is minimization problem
  constraintArray=[]
  lineCount=len(ilpArray[0])
  for i in range(lineCount): #Creating array that handles the subject to part of our ilp problem
    tempArray=[]  
    for j in range(numOfTestCases):
      if(ilpArray[j+1][i]==-1):
        break
      else:
        tempArray.append(ilpArray[j+1][i])
    coefficientArray=[]
    for k in range(len(tempArray)):
      coefficientArray.append(1)
    secondTempArray=[]
    secondTempArray.append(tempArray)
    secondTempArray.append(coefficientArray)
    constraintArray.append(secondTempArray)
  rightHandSideArray = []
  constraintSenses=[] 
  for i in range(lineCount): #setting the >=1 part of our cosntraint parts
    rightHandSideArray.append(1)
    constraintSenses.append("G")
  cplexObject.linear_constraints.add(lin_expr= constraintArray,senses= constraintSenses,rhs= rightHandSideArray)
  cplexObject.solve()
  print("Obj Value:",cplexObject.solution.get_objective_value())
  solnArray=cplexObject.solution.get_values()
  print("Values of Decision Variables:",solnArray)
  finalTestCaseValues=[]
  for i in range(len(solnArray)):
    if(solnArray[i]!=0.0):
      finalTestCaseValues.append("T"+str(i+1))
  print("IDs of the minimum number of selected test cases that covers all the module lines: ",finalTestCaseValues)

    


ilpArray = generateTwoDimArray()
solveILP(ilpArray)



