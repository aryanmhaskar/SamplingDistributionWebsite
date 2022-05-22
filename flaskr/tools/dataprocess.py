import os
import numpy as np
from scipy.stats import bernoulli, norm, poisson
import statistics
from scipy import stats
from scipy.stats import kurtosis, skew
import seaborn as sns
import matplotlib.pyplot as plt
import os

def mean_distribution(id, data:list, num_samples:int, sample_size:int):
    rs = []
    for i in range(num_samples):
        rs.append(np.random.choice(data, sample_size))
    rs = np.array(rs)
    x_bar = rs.mean(axis=1)
    plt.hist(x_bar);
    plt.savefig(os.path.join(os.path.dirname(__file__), ("../static/" + str(id) + 'mean.png')))

def stdev_distribution(id, data:list, num_samples:int, sample_size:int):
    rs = []
    for i in range(num_samples):
        rs.append(np.random.choice(data, sample_size))
    rs = np.array(rs)
    x_bar = rs.std(axis=1)
    plt.hist(x_bar);
    plt.savefig(os.path.join(os.path.dirname(__file__), ("../static/" + str(id) + 'stdev.png')))