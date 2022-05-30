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
import csv

class Data_Processor:
    
    def __init__(self, id, data:list, num_samples, sample_size):
        self.whole_data = []
        self.summary_data = []
        self.stat_distribution(id, data, num_samples, sample_size)
        
    def stat_distribution(self, id, data:list, num_samples:int, sample_size:int):
        new_data = []
        for point in data:
            new_data.append(float(point))
        rs = []
        for i in range(int(num_samples)):
            thing = np.random.choice(new_data, int(sample_size), replace=True)
            amogus = [("Trial" + i)]
            amogus.append(thing)
            rs.append(thing)
            self.whole_data(amogus)
        
        rs = np.array(rs)

        count = 1
        headers = [""]
        for amongus in rs:
            headers.append("Trial" + count)
            count += 1
        self.summary_data.append(headers)

        # Compute means, generate distribution, and add to summary statistics array
        means = []
        named_means = ["Mean"]
        for sub in rs:
            means.append(sub.mean())
        self.summary_data.append(named_means.append(means))
        means = np.array(means)
        plt.hist(means);
        plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'mean.png')))

        # Compute standard deviation, generate distribution, and add to summary statistics array
        stdvs = []
        named_stdevs = ["Standard Deviation"]
        for sub in rs:
            stdvs.append(sub.std())
        self.summary_data(named_stdevs.append(stdvs))
        stdvs = np.array(stdvs)
        plt.hist(stdvs);
        plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'stdev.png')))

        # Compute ranges, generate distribution, and add to summary statistics array
        ranges = []
        named_ranges = ["Range"]
        for sub in rs:
            ranges.append(sub.max() - sub.min())
        self.summary_data(named_ranges.append(ranges))
        ranges = np.array(ranges)
        plt.hist(ranges);
        plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'range.png')))

        with open('/uploads/summary' + str(id) + '.csv','wb') as myfile:
            wr = csv.writer(myfile) #, quoting=csv.QUOTE_ALL)
            wr.writerows(self.summary_data)

        with open('/uploads/all' + str(id) + '.csv','wb') as myfile:
            wr = csv.writer(myfile) #, quoting=csv.QUOTE_ALL)
            wr.writerows(self.whole_data)

    def distribution(self, id, data:list):
        new_data = []
        for point in data:
            new_data.append(float(point))
        plt.hist(new_data)
        plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'dist.png')))

    def statistics_info(self, data:list):
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

Data_Processor.mean_distribution(1, [3, 4, 5, 2.0, 4.5, 6.5], 2, 2);