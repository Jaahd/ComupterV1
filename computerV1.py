
# regex to match the entire polynominal, to check if the syntax is correct
checkLineRegex = r"^(([+-]?)\s*(\d+[\.,]?\d*)\s*(\*?\s*[xX]\s*\^\s*(\d+)\s*|\*?\s*[xX]\s*)?)+=(([+-]?)\s*(\d+[\.,]?\d*)\s*(\*?\s*[xX]\s*\^\s*(\d+)\s*|\*?\s*[xX]\s*)?)+$"

# regex to get each of the relevant portions of the polynominal
regex = r"(([+-]?)\s*(\d+[\.,]?\d*)\s*(\*?\s*x\s*\^\s*(\d+)\s*|\*?\s*x\s*)?)"



'''
    computerV1Usage: usage display when the script hasn't been called correctly

'''
def computerV1Usage(nbArgs):
    import sys

    if nbArgs == 1:
        print("\nComputerV1: Too few arguments")
    elif nbArgs > 2:
        print("\nComputerV1: Too many arguments")
    elif nbArgs == -1:
        print("ComputerV1: The syntax of the polynominal is incorrect, please \
check again:")

    print("\nUsage:\n\n\tpython ComputerV1.py \"<equation>\"\n")
    print("equation format:\n\t\"c * X^0 + b * X^1 + a * X^2\"")
    print("\t\"c + b * X + a * x^2\"")
    print("\t\twith a, b and c or more to be positive or negative intergers or \
floats\n")

    sys.exit()



'''
    sqrRoot: return the square root of a given number, with a precision of 1/10

'''
def sqrRoot(num, prec = None):

    if not prec:
        prec = 0.0000000001

    if num < 0:
        num = -num
        i = 1

    root = num
    while (root - float(num / root)) > prec:
        root = float((root + float(num / root)) / 2)

    return root



'''
    absVal: return the absolute value of the given number

'''
def absVal(nb):

    ret = nb if nb > 0 else nb * -1

    return formatNb(ret)



'''
    formatNb: remove trailling zeros from float numbers

'''
def formatNb(nb):
    from decimal import Decimal

    return '%g' % (Decimal(str(nb)))



'''
    checkSyntax: check the correctness of the given polynominal

'''
def checkSyntax(args):
    import re

    print("\nGiven equation: %s" % args)

    patern = re.compile(checkLineRegex)

    if not patern.match(args):
        computerV1Usage(-1)



'''
    getCoefNDegree: get the coef and the degree of each part of the polynominal

'''
def getCoefNDegree(ret, argStr, sign):
    import re

    posMatches = re.findall(regex, argStr, re.IGNORECASE)

    for elt in posMatches:

        if elt[3] and elt[4]:
            key = int(elt[4])
        elif elt[3]:
            key = 1
        else:
            key = 0

        val = elt[2].replace(',', '.')
        val = (float(val) * (-1 * sign[0]) if elt[1] == '-' else
               float(val) * (-1 * sign[1]))
        ret[key] = val if key not in ret else ret[key] + val



'''
    checkAgrs: create a dictionary containing each degree in the polynominal
               and their coeficiant

'''
def createDict(argStr):
    import re, sys
    from collections import OrderedDict

    patern = re.compile(regex)

    argStr1, argStr2 = argStr.split('=')

    dict = {}
    getCoefNDegree(dict, argStr1, [1, -1])
    getCoefNDegree(dict, argStr2, [-1, 1])

    dict = {k: v for k, v in dict.items() if v != 0}

    return OrderedDict(sorted(dict.items()))



'''
    printReducForm: print the reduced form of the polynominal and its degree

'''
def printReducForm(ordDict):

    toPrint = "Reduced form:  "
    for elt in ordDict:
        if elt >= 0:
            if ordDict[elt] < 0:
                toPrint += " -"
            if elt > 0 and ordDict[elt] > 0:
                toPrint += " +"
            valAbs = absVal(ordDict[elt])
            toPrint += " %s" % valAbs
        if elt > 0:
            toPrint += " * X"
        if elt > 1:
            toPrint += "^%d" %elt

    toPrint += " = 0"

    print("%s\n" % toPrint)

    polyDegree = max(ordDict, key=int)
    print("Polynominal degree: %d\n" % polyDegree)

    return polyDegree



'''
    degree2Solutions: display the results when the polynominal degree is 2

'''
def degree2Solutions(ordDict):

    a = 0 if 2 not in ordDict else ordDict[2]
    b = 0 if 1 not in ordDict else ordDict[1]
    c = 0 if 0 not in ordDict else ordDict[0]

    delta = (b * b) - (4 * a * c)

    if delta > 0:
        if a:
            root = sqrRoot(delta)
            x1 = (-b - root) / (2 * a)
            x2 = (-b + root) / (2 * a)
            print("The discriminant, %s, is stricly positive, the polynominal \
has 2 real solutions:\n\t%s\n\t%s\n" % (formatNb(delta), formatNb(x1), formatNb(x2)))

    if delta == 0:
        x = -b / (2 * a)
        print("The discriminant is 0, the only solution is: %s\n" % formatNb(x))

    if delta < 0:
        x1 = -b /(2 * a)
        x2 = sqrRoot(delta) / (2 * a)
        print("The discriminant, %s, is stricly negative, the polynominal has 2\
 complexe solutions:\n\t%s + i * %s\n\t%s - i * %s\n" \
% (formatNb(delta), formatNb(x1), formatNb(x2), formatNb(x1), formatNb(x2)))



'''
    degree1Solution: display the result when the polynominal degree is 1 or less

'''
def degree1Solution(ordDict):

    a = 0 if 1 not in ordDict else ordDict[1]
    b = 0 if 0 not in ordDict else ordDict[0]

    if a == 0:
        print("All the real numbers are solutions for this polynominal.\n")
    else:
        x = -b / a
        print("The only solution for this polynominal is: %s.\n" % formatNb(x))



if __name__ == '__main__':
    import sys

    args = sys.argv

    if len(args) != 2:
        computerV1Usage(len(args))

    checkSyntax(args[1])

    ordDict = createDict(args[1])

    polyDegree = printReducForm(ordDict)

    if polyDegree > 2:
        print("\nComputerV1: The polynamial degree is strictly greater than 2, \
I can't solve the equation\n")
    elif polyDegree == 2:
        degree2Solutions(ordDict)
    else:
        degree1Solution(ordDict)
