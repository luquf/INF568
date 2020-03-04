from factoring import *
from random import randint
from json import dumps


def parse_challenge(filename="challenge/leo-berton.chall"):
    f = open(filename, "r")
    lines = f.read()
    lines = lines.split("\n")
    lines = lines[1:len(lines)-1]
    for l in lines:
        if l[0] == "#":
            lines.remove(l)
    return [int(l) for l in lines]

if __name__ == "__main__":
    numbers = parse_challenge()
    filename = "results/challenge-"+str(randint(0, 1000))+".results"
    print("Results will be in file", filename)
    for i in range(0, len(numbers)):
        print("Let's factor", numbers[i])
        res = factorization(numbers[i])
        if str(res["status"]) == "success":
            print("Found factors:", res["factors"], "in", res["time"], "seconds")
            f = open(filename, "a+")
            f.write("SUCCESSFULL FACTORING\n") 
            f.write("Number:" + str(numbers[i]) + "\n")
            f.write("Factors: " + dumps(res["factors"]) + "\n")
            f.write("Base point: X = " + str(res["coords"][0]) + " Z = " + str(res["coords"][1]) + "\n")
            f.write("A parameter: " + str(res["aparameter"]) + "\n")
            f.write("ECM trial smoothness: " + str(res["beta"]) + "\n")
            f.write("Upper bound: " + str(res["upper_bound"]) + "\n")
            f.write("Finding bound: " + str(res["bound"]) + "\n")
            f.write("Step: " + str(res["step"]) + "\n")
            f.write("Time: " + str(res["time"]) + " seconds\n")
            f.write("\n\n")
            f.close()
        elif str(res["status"]) == "trial":
            print("Found factors without ECM")
            f = open(filename, "a+")
            f.write("SUCCESSFULL FACTORING WITHOUT ECM\n")
            f.write("Number:" + str(numbers[i]) + "\n")
            f.write("Factors: " + dumps(res["factors"]) + "\n")
            f.write("\n\n")
            f.close()
            
