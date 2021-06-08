import random
import numpy as np
import struct
from codecs import decode


def int_to_bytes(n, length):
    return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]


def bin_to_float(b):
    bf = int_to_bytes(int(b, 2), 8)
    return struct.unpack('>d', bf)[0]


def float_to_bin(value):
    [d] = struct.unpack(">Q", struct.pack(">d", value))
    return '{:064b}'.format(d)


class Individual:
    f = None

    def __init__(self, minX, maxX, minY, maxY):
        self.x = random.uniform(minX, maxX)
        self.y = random.uniform(minY, maxY)
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def checkValues(self):
        if self.x < self.minX:
            self.x = self.minX
        if self.y < self.minY:
            self.y = self.minY
        if self.x > self.maxX:
            self.x = self.maxX
        if self.y > self.maxY:
            self.y = self.maxY


class GenAlgo:

    def __init__(self, minX, maxX, minY, maxY, sizePopul: int, maxIters: int, children: int, probMutation):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.sizePopul = sizePopul
        self.maxIters = maxIters
        self.numberChildren = children
        self.probabilityMutation = probMutation
        self.population = []

    @staticmethod
    def objectiveFunction(x, y):
        return np.sin((x+1)**2 + y**2)/((x+1)**2 + y**2)

    def generation(self):
        for i in range(self.sizePopul):
            self.population.append(Individual(self.minX, self.maxX, self.minY, self.maxY))
            self.population[i].f = self.objectiveFunction(self.population[i].x, self.population[i].y)

    def write(self):
        i = 1
        for tmp in self.population:
            print(f"{i}: x = {tmp.x}, y = {tmp.y}, f = {tmp.f}")
            i += 1
        print()

    def sort(self):
        self.population.sort(key=lambda tmp: -tmp.f)

    def selection(self):
        a = random.uniform(1, 2)
        b = 2 - 1
        for i in range(self.sizePopul - 2, 0, -1):
            pi = (a - (a - b) * (i - 1) / (self.sizePopul - 1)) / a
            if random.uniform(0, 1) > pi:
                self.population.pop(i)

    def crossover(self):
        needSize = min(self.sizePopul - len(self.population), self.numberChildren)
        if needSize == 0:
            return
        length = len(self.population)

        for i in range(0, length):
            for j in range(i + 1, length):
                pivot = int(64 * np.exp(self.population[i].f) / (np.exp(self.population[i].f) + np.exp(self.population[j].f)))

                bin1X = float_to_bin(self.population[i].x)
                bin1Y = float_to_bin(self.population[i].y)
                bin2X = float_to_bin(self.population[j].x)
                bin2Y = float_to_bin(self.population[j].y)

                child1 = Individual(self.minX, self.maxX, self.minY, self.maxY)
                child1.x = bin_to_float(bin1X[0:pivot] + bin2X[pivot:64])
                child1.y = bin_to_float(bin1Y[0:pivot] + bin2Y[pivot:64])
                child1.checkValues()
                child1.f = self.objectiveFunction(child1.x, child1.y)
                self.population.append(child1)
                needSize -= 1
                if needSize == 0:
                    return

                child2 = Individual(self.minX, self.maxX, self.minY, self.maxY)
                child2.x = bin_to_float(bin2X[0:pivot] + bin1X[pivot:64])
                child2.y = bin_to_float(bin2Y[0:pivot] + bin1Y[pivot:64])
                child2.checkValues()
                child2.f = self.objectiveFunction(child2.x, child2.y)
                self.population.append(child2)
                needSize -= 1
                if needSize == 0:
                    return

    def clean(self):
        self.population = list(set(self.population))

    def mutation(self):
        for i in range(1, len(self.population) - 1):
            if random.uniform(0, 1) < self.probabilityMutation:
                binX = float_to_bin(self.population[i].x)
                binY = float_to_bin(self.population[i].y)

                pivot = random.randint(3, 63)

                self.population[i].x = bin_to_float(binX[0:pivot]+str(int(not(bool(int(binX[pivot])))))+binX[pivot+1:64])
                self.population[i].y = bin_to_float(binY[0:pivot]+str(int(not(bool(int(binY[pivot])))))+binY[pivot+1:64])

                self.population[i].checkValues()
                self.population[i].f = self.objectiveFunction(self.population[i].x, self.population[i].y)

    def newIndividuals(self):
        while len(self.population) != self.sizePopul:
            new = Individual(self.minX, self.maxX, self.minY, self.maxY)
            new.f = self.objectiveFunction(new.x, new.y)
            self.population.append(new)

    def genetic(self):
        iter = 0
        self.generation()
        self.sort()

        while iter != self.maxIters:
            iter += 1
            self.selection()
            self.crossover()
            self.clean()
            self.mutation()
            self.newIndividuals()
            self.sort()

        return self.population[0]

