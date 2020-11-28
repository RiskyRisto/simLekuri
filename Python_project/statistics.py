# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 12:29:49 2020

@author: Mika Sipilä
"""

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics import tsaplots

def calculate_and_print_statistics(data):
    blocking_times = []
    entrance_mean_queues = []
    utilization_rates = []

    for data_for_config in data:
        blocking_times.append(list(map(lambda sample: float(sample["mean_blocking_time"]), data_for_config)))
        entrance_mean_queues.append(list(map(lambda sample: float(sample["mean_queue_at_entrance"]), data_for_config)))
        utilization_rates.append(list(map(lambda sample: float(sample["utilization_rate_of_operation_theatre"]), data_for_config))) 

    # Increase N_SAMPLES from settings to atleast 40 (preferably 1000) and run this section
    # We can not assume variables with normal distribution so it is better to use non-parametric estimation.
    # If the confidence interval of difference doesn't include 0, difference is statistically significant.
    for i in range(len(data)):

        mean_queue_at_entrance = np.mean(entrance_mean_queues[i])
        entrance_mean_queue_ci = calculate_95_ci(entrance_mean_queues[i])
        mean_utilization_rate = np.mean(utilization_rates[i])
        mean_utilization_rate_ci = calculate_95_ci(utilization_rates[i])

        print("Statistics for hospital", i + 1)
        print("Mean of mean queues at entrance: %.3f" % (mean_queue_at_entrance))
        print("95 %% Confidence interval for mean of mean queues at entrance: [%.3f, %.3f]" % (entrance_mean_queue_ci[0], entrance_mean_queue_ci[1]))
        print("Mean of utilization rates: %.3f" % (mean_utilization_rate))
        print("95 %% Confidence interval for utilization rates: [%.3f, %.3f]" % (mean_utilization_rate_ci[0], mean_utilization_rate_ci[1]))
        print("-" * 20)

    #2-compinations 
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            blocking_time_differences = np.array(blocking_times[i]) - np.array(blocking_times[j])
            entrance_queue_differences = np.array(entrance_mean_queues[i]) - np.array(entrance_mean_queues[j])
            utilization_rate_differences = np.array(utilization_rates[i]) - np.array(utilization_rates[j])
            
            mean_blocking_time_difference = np.mean(blocking_time_differences)
            blocking_time_difference_ci = calculate_95_ci(blocking_time_differences)
            mean_queue_at_entrance_difference = np.mean(entrance_queue_differences)
            entrance_mean_queue_difference_ci = calculate_95_ci(entrance_queue_differences)
            mean_utilization_rate_difference = np.mean(utilization_rate_differences)
            mean_utilization_rate_difference_ci = calculate_95_ci(utilization_rate_differences)

            print("Differences between hospital%i and hospital%i" % (i + 1, j + 1))
            print("Difference of means of blocking time: %.3f" % (mean_blocking_time_difference))
            print("95 %% Confidence interval for difference of means of blocking times: [%.3f, %.3f]" % (blocking_time_difference_ci[0], blocking_time_difference_ci[1]))
            print("Difference of means of mean queues at entrance: %.3f" % (mean_queue_at_entrance_difference))
            print("95 %% Confidence interval for difference of means of mean queues at entrance: [%.3f, %.3f]" % (entrance_mean_queue_difference_ci[0], entrance_mean_queue_difference_ci[1]))
            print("Difference of means of utilization rates: %.3f" % (mean_utilization_rate_difference))
            print("95 %% Confidence interval for difference of utilization rates: [%.3f, %.3f]" % (mean_utilization_rate_difference_ci[0], mean_utilization_rate_difference_ci[1]))
            print("-" * 20)

def calculate_95_ci(data):
    lower_index = round(len(data)*0.025)
    upper_index = round(len(data)*0.975)
    if lower_index <= 1:
        lower_index = 2
    if upper_index >= len(data) - 1:
        upper_index = len(data) - 2
    lower_limit = sorted(data)[lower_index - 1]
    upper_limit = sorted(data)[upper_index - 1]
    return([lower_limit, upper_limit])

def acf_plots(data):
    n_rows = int(len(data)/3)
    if n_rows < 0:
        n_rows = 1
    n_cols = int(len(data)/n_rows)
    if n_rows*n_cols < len(data):
        n_cols += 1
    plt.figure(figsize = (16,8))
    plt.suptitle('Autocorrelations and 95% confidence intervals of no autocorrelation', fontsize=12)
    for i in range(len(data)):
        plt.subplot(n_rows, n_cols, i + 1)
        acf,confint = tsaplots.acf(data[i]["entrance_queue_timeseries"], nlags=100, alpha=0.05,fft=False)
        plt.plot(range(0, 101), acf, 'ob')
        plt.fill_between(range(0, 101), (confint[:,0] - acf), (confint[:,1] - acf), color='b', alpha=.1)
        plt.title("Sample %i" % (i + 1))
        plt.xlabel('Lag (1 = 10 time steps)')
        plt.ylabel('Autocorrelation')
        plt.ylim((-1.05,1.05))
        plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.show()

    