#!/usr/bin/python3
import re
import sys

from collections import OrderedDict
from decimal import Decimal

# regex to match the entire polynominal, to check if the syntax is correct
checkLineRegex = r"^(([+-]?)\s*(\d*[\.,]?\d*)\s*(\*?\s*[xX]\s*\^\s*(\d+)\s*|\*?\s*[xX]\s*)?)+=(([+-]?)\s*(\d+[\.,]?\d*)\s*(\*?\s*[xX]\s*\^\s*(\d+)\s*|\*?\s*[xX]\s*)?)+$"

# regex to get each of the relevant portions of the polynominal
regex = r"(([+-]?)\s*(\d*[\.,]?\d*)\s*(\*?\s*x\s*\^\s*(\d+)\s*|\*?\s*x\s*)?)"


def computerV1Usage(nbArgs):
    ''' computerV1Usage: usage display when the script hasn't been called correctly '''

    if nbArgs == 1:
        print("\nComputerV1: Too few arguments")
    elif nbArgs > 2:
        print("\nComputerV1: Too many arguments")
    elif nbArgs == -1:
        print("ComputerV1: The syntax of the polynominal is incorrect, please check again:")

    print("\nUsage:\n\n\tpython ComputerV1.py \"<equation>\"\n")
    print("equation format:\n\t\"EXPR = EXPR\"")
    print("EXPR format:\n\t\"c * X^0 + b * X^1 + a * X^2\"")
    print("\t\"c + b * X + a * x^2\"")
    print("\t\twith a, b and c or more to be positive or negative intergers or floats\n")

    sys.exit()


def sqrRoot(num, prec = None):
    ''' sqrRoot: return the square root of a given number, with a precision of 1/10 '''

    if not prec:
        prec = 0.0000000001

    if num < 0:
        num = -num
        i = 1

    root = num
    while (root - float(num / root)) > prec:
        root = float((root + float(num / root)) / 2)

    return root


def absVal(nb):
    ''' absVal: return the absolute value of the given number '''

    ret = nb if nb > 0 else nb * -1

    return formatNb(ret)


def formatNb(nb):
    ''' formatNb: remove trailling zeros from float numbers '''


    return '%g' % (Decimal(str(nb)))


def checkSyntax(args):
    ''' checkSyntax: check the correctness of the given polynominal '''
    toPrint = "\nGiven equation: "
    for char in args:
        if char in "+*=":
            toPrint += ' '
        if not char.isspace():
            if char.isalpha():
                toPrint += char.upper()
            else:
                toPrint += char
        if char in "+*=":
            toPrint += ' '
    print(toPrint)
    patern = re.compile(checkLineRegex)

    if not patern.match(args):
        computerV1Usage(-1)



def getCoefNDegree(ret, argStr, sign):
    ''' getCoefNDegree: get the coef and the degree of each part of the polynominal '''

    posMatches = re.findall(regex, argStr, re.IGNORECASE)

    for elt in posMatches:

        if elt[3] and elt[4]:
            key = int(elt[4])
        elif elt[3]:
            key = 1
        else:
            key = 0

        val = 0
        if (elt[3] and elt[2]) or (elt[2] and not elt[3]):
            val = elt[2].replace(',', '.')
            val = (float(val) * (-1 * sign[0]) if elt[1] == '-' else
                   float(val) * (-1 * sign[1]))
        elif elt[3]:
            val = 1

        ret[key] = val if key not in ret else ret[key] + val


def createDict(argStr):
    ''' checkAgrs: create a dictionary containing each degree in the polynominal
        and their coeficiant
    '''

    patern = re.compile(regex)

    argStr1, argStr2 = argStr.split('=')

    dict = {}
    getCoefNDegree(dict, argStr1, [1, -1])
    getCoefNDegree(dict, argStr2, [-1, 1])

    dict = {k: v for k, v in dict.items() if v != 0}

    return OrderedDict(sorted(dict.items()))


def printReducForm(ordDict):
    ''' printReducForm: print the reduced form of the polynominal and its degree '''

    if not ordDict:
        print("Polynominal degree: 0\n")
        return 0

    toPrint = "\nReduced form:  "
    tmp = ""
    for elt in ordDict:

        if elt >= 0:
            if ordDict[elt] < 0:
                tmp += " -"
            if elt > 0 and ordDict[elt] > 0 and tmp != "":
                tmp += " +"
            valAbs = absVal(ordDict[elt])
            tmp += " %s" % valAbs
        if elt > 0:
            tmp += " * X"
        if elt > 1:
            tmp += "^%d" %elt

    if tmp != "":
        toPrint += tmp

    toPrint += " = 0"
    print(toPrint)

    polyDegree = max(ordDict, key=int)
    print("Polynominal degree: %d\n" % polyDegree)

    return polyDegree



def degree2Solutions(ordDict):
    ''' degree2Solutions: display the results when the polynominal degree is 2 '''

    a = 0 if 2 not in ordDict else ordDict[2]
    b = 0 if 1 not in ordDict else ordDict[1]
    c = 0 if 0 not in ordDict else ordDict[0]

    delta = (b * b) - (4 * a * c)

    deltaStr = "(%s)^2 - (4 * %s * %s)" % (b, a, c)
    if delta > 0:
        if a:
            root = sqrRoot(delta)
            x1 = (-b - root) / (2 * a)
            x2 = (-b + root) / (2 * a)
            print("The discriminant: %s = %s, is stricly positive, the polynominal \
has 2 real solutions:\n\t%s\n\t%s\n" % (deltaStr, formatNb(delta), formatNb(x1), formatNb(x2)))

    if delta == 0:
        x = -b / (2 * a)
        xStr = "(-1 * %s) / (2 * %s)" % (b, a)
        print("The discriminant: %s = 0, is zero, the only solution is: %s = %s\n" % (deltaStr, xStr, formatNb(x)))

    if delta < 0:
        x1 = -b /(2 * a)
        x2 = sqrRoot(delta) / (2 * a)
        print("The discriminant, %s = %s, is stricly negative, the polynominal has 2 \
complexe solutions:\n\t%s + i * %s\n\t%s - i * %s\n" \
% (deltaStr, formatNb(delta), formatNb(x1), formatNb(x2), formatNb(x1), formatNb(x2)))



def degree1Solution(ordDict):
    ''' degree1Solution: display the result when the polynominal degree is 1 or less '''

    a = 0 if 1 not in ordDict else ordDict[1]
    b = 0 if 0 not in ordDict else ordDict[0]

    if a == 0:
        if ordDict and ordDict[0] != 0:
            print("There are no solution for this polynominal.\n")
        else:
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
