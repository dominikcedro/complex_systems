"""
author: Dominik Cedro
date: 23.11.2024
description: implement oslo model based on instruction from lab3
"""
import numpy as np
import matplotlib.pyplot as plt

class OsloModel:
    def __init__(self, L, p=0.5):
        self.length = L
        self.prob = p
        self.heights = [i * 0 for i in range(L)]
        self.thresh = np.random.choice([1, 2], size=L, p=[1 - p, p])
        self.avalanches = []

    def add_grain(self):
        self.heights[0] += 1
        self.relax()

    def relax(self):
        avalanche_size = 0
        while np.any(self.heights > self.thresh):
            for i in range(self.length):
                if self.heights[i] > self.thresh[i]:
                    avalanche_size += 1
                    if i == 0:
                        self.heights[i] -= 2 # why does it have to be 2???
                        self.heights[i + 1] += 1
                    elif i == self.length - 1:
                        self.heights[i] -= 1
                        self.heights[i - 1] += 1
                    else:
                        self.heights[i] -= 2
                        self.heights[i + 1] += 1
                        self.heights[i - 1] += 1
                    self.thresh[i] = np.random.choice([1, 2], p=[1 - self.prob, self.prob])
        self.avalanches.append(avalanche_size)

    def run(self, steps):
        for _ in range(steps):
            self.add_grain()

    def plot_avalanche_size(self):
        s_max = max(self.avalanches)
        scaled_avalanches = [s / s_max for s in self.avalanches]
        plt.plot(scaled_avalanches)
        plt.xlabel('Time (grain additions)')
        plt.ylabel('Scaled Avalanche Size (s/s_max)')
        plt.title('Scaled Avalanche Size vs Time')
        plt.show()

    def plot_avalanche_probability(self, lengths):
        for L in lengths:
            self.__init__(L)
            self.run(10000)
            avalanche_sizes, counts = np.unique(self.avalanches, return_counts=True)
            probabilities = counts / sum(counts)
            plt.loglog(avalanche_sizes, probabilities, linestyle="--",label=f'L={L}')
        plt.xlabel(f'Avalanche Size (s)')
        plt.ylabel(f'Probability P(s, L)')
        plt.title('Avalanche Size Probability')
        plt.legend()
        plt.show()


L = 100
steps = 10000
oslo = OsloModel(L)
oslo.run(steps)
oslo.plot_avalanche_size()

L = 500
oslo = OsloModel(L)
oslo.run(steps)
oslo.plot_avalanche_size()

lengths = [100, 150, 250, 300, 500]
oslo.plot_avalanche_probability(lengths)