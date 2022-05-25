from dataclasses import dataclass
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
    new_data = []
    for point in data:
        new_data.append(int(float(point)))
    rs = []
    for i in range(int(num_samples)):
        rs.append(np.random.choice(new_data, int(sample_size)))
    rs = np.array(rs)
    x_bar = rs.mean()
    plt.hist(x_bar);
    plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'mean.png')))

def stdev_distribution(id, data:list, num_samples:int, sample_size:int):
    new_data = []
    for point in data:
        new_data.append(int(float(point)))
    rs = []
    for i in range(int(num_samples)):
        rs.append(np.random.choice(np.array(new_data), int(sample_size)))
    rs = np.array(rs)
    x_bar = rs.std()
    plt.hist(x_bar);
    plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'stdev.png')))

def distribution(id, data:list):
    new_data = []
    for point in data:
        new_data.append(int(float(point)))
    plt.hist(new_data)
    plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'dist.png')))

def statistics_info(data:list):
    for i in range(0, len(data)):
        data[i] = float(data[i])
    total = 0;
    for num in data:
        total += float(num)
    mean = total/len(data)
    return f"""The mean of the dataset is: {mean}
    The standard deviation of the dataset is: {statistics.pstdev(data)} 
    The max of the dataset is: {max(data)}
    The min of the dataset is: {min(data)}
    The range of the dataset is: {max(data) - min(data)} """
