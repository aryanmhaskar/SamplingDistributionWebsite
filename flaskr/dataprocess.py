from dataclasses import dataclass
import os
import numpy as np
from scipy.stats import bernoulli, norm, poisson
import statistics
from scipy import stats
from scipy.stats import kurtosis, skew
import seaborn as sns
import matplotlib as mpl
mpl.use('Agg')
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
            amogus = [("Trial" + str(i + 1))]
            for item in thing:
                amogus.append(item)
            rs.append(thing)
            self.whole_data.append(amogus)
        
        rs = np.array(rs)

        count = 1
        headers = [""]
        for amongus in rs:
            headers.append("Trial" + str(count))
            count += 1
        self.summary_data.append(headers)

        # Compute means, generate distribution, and add to summary statistics array
        means = []
        named_means = ["Mean"]
        for sub in rs:
            means.append(sub.mean())
        for item in means:
            named_means.append(item)
        
        self.summary_data.append(named_means)
        means = np.array(means)
        plt.hist(means);
        plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'mean.png')))

        # Compute standard deviation, generate distribution, and add to summary statistics array
        stdvs = []
        named_stdevs = ["Standard Deviation"]
        for sub in rs:
            stdvs.append(sub.std())

        for item in stdvs:
            named_stdevs.append(item)

        self.summary_data.append(named_stdevs)
        stdvs = np.array(stdvs)
        plt.hist(stdvs);
        plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'stdev.png')))

        # Compute ranges, generate distribution, and add to summary statistics array
        ranges = []
        named_ranges = ["Range"]
        for sub in rs:
            ranges.append(sub.max() - sub.min())
    
        for item in ranges:
            named_ranges.append(item)

        self.summary_data.append(named_ranges)
        ranges = np.array(ranges)
        plt.hist(ranges);
        plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'range.png')))

        with open(os.path.join(os.path.dirname(__file__), ('./uploads/summary' + str(id) + '.csv')),'w') as myfile:
            wr = csv.writer(myfile) #, quoting=csv.QUOTE_ALL)
            wr.writerows(self.summary_data)

        with open(os.path.join(os.path.dirname(__file__), ('./uploads/all' + str(id) + '.csv')),'w') as myfile:
            wr = csv.writer(myfile) #, quoting=csv.QUOTE_ALL)
            wr.writerows(self.whole_data)

    def distribution(self, id, data:list):
        new_data = []
        for point in data:
            new_data.append(float(point))
        plt.hist(new_data)
        plt.savefig(os.path.join(os.path.dirname(__file__), ("./static/" + str(id) + 'dist.png')))

    def statistics_info(data:list):
        for i in range(0, len(data)):
            data[i] = float(data[i])
        total = 0;
        for num in data:
            total += float(num)
        mean = total/len(data)
        return f"""The true mean of the dataset is: {mean}
        The true standard deviation of the dataset is: {statistics.pstdev(data)} 
        The true max of the dataset is: {max(data)}
        The true min of the dataset is: {min(data)}
        The true range of the dataset is: {max(data) - min(data)} """
