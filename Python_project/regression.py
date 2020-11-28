import numpy as np
import main
import json

import settings
import Hospital
from helpers import exp, unif

"""
Build a regression model for the average queue length. 
Which structural parameters affect the queue length significantly?
        "n_preparation_rooms": 4,
        "n_recovery_rooms": 4,
        "cancelling_prob": CANCELLING_PROBABILITY,
        "preparation_time_random_stream": exp(40),
        "recovery_time_random_stream": unif(30,50),
        "interarrival_time_random_stream": exp(25)

determine if some b[i] == 0

Does the model make any sense (or are joint effects essential to take in to account in the model)?
"""

class RegressionModel:
    """
    Linear regression model
    """
    def __init__(self):
        self.beta = None

    def fit(self, X, y, verbose = False):
        """
        Find optimal parameters using least squares
        Params:
            X: numpy ndarray (number of examples, number of explanatory variables)
            y: numpy ndarray (number of dependent variables,)
        Returns:
            least squared solution
        Raises: 
            LinAlgError("Singular matrix")
        """
        #add intercept
        X = self.expandedX(X)
        #@ is a general matrix multiplication / dot product operator in numpy
        self.beta = np.linalg.inv(X.T @ X) @ X.T @ y
        if verbose:
            print(f"beta {self.beta}")

    def expandedX(self, X):
        """
        Add the "intercept term" as first column to the matrix
        """
        intercept = np.ones(len(X))
        return np.column_stack((intercept, X))

    def predict(self,X):
        """
        Evaluate model using calculated coefficients
        Params:
            X: numpy ndarray (number of examples, number of explanatory variables)
        Returns:
            numpy ndarray (number of examples, 1)
        """
        
        return self.expandedX(X) @ self.beta

    def mse(self, X, y):
        """
        Calculate mean squared error for data
        """
        predicted_y = self.predict(X)
        difference = predicted_y - y
        error = difference @ difference
        return (1 / len(X)) * error

    def r2(self, X, y):
        """
        Calculates the r-squared measure
        Tells what percentage of the variance of y this
        regression model explains
        Thus, R2 = 1 indicates that the fitted model explains all variability in 
        y, while R2 = 0 indicates no 'linear' relationship
        """
        SStot = np.sum((y - y.mean())**2)
        SSres = np.sum((y - self.predict(X))**2)
        return 1 - SSres / SStot

    def __str__(self):
        with np.printoptions(precision=3, suppress=True):
            s = "beta {}".format(self.beta)
        return s

    @classmethod
    def crossValidate(cls, X, y):
        """
        Leave one out cross validation
        """
        error = 0
        model = RegressionModel()
        #take one row at the time from the dataset into validation
        #and add error to total
        for i in range(len(X)):
            Xout = X[i:i+1]
            yout = y[i:i+1]
            Xin = np.delete(X, i, axis=0)
            yin = np.delete(y, i, axis=0)
            model.fit(Xin, yin)
            y_predicted = model.predict(Xout)
            error += (yout - y_predicted) ** 2.0

        error = error / len(X)
        return error

def getMapping(ex):
    """
    Params:
        ex: list(int) indices of corresponding variables
    """
    inter_dist = [exp, unif]
    inter_time = [25, 22.5]
    inter = [
        [exp(25), exp(22.5)], 
        [unif(20,30), unif(20,25)]
    ]
    prep = [exp(40), unif(30,50)]
    rec = [exp(40), unif(30,50)]
    n_prep = [4,5]
    n_rec = [4,5]

    interarrival_stream = inter[ex[0]][ex[1]]
    config = {
        "interarrival_time_random_stream": interarrival_stream,
        "preparation_time_random_stream": prep[ex[2]],
        "recovery_time_random_stream": rec[ex[3]],
        "n_preparation_rooms": n_prep[ex[4]],
        "n_recovery_rooms": n_rec[ex[5]],
        "cancelling_prob": settings.CANCELLING_PROBABILITY
    }

    return config

def getConfigs():
    """
    All 64 
    """
    designMatrix = []
    n_choices = 2
    for a in range(n_choices):
        for b in range(n_choices):
            for c in range(n_choices):
                for d in range(n_choices):
                    for e in range(n_choices):
                        for f in range(n_choices):
                            designMatrix.append([a,b,c,d,e,f])
    configs = []

    for ex in designMatrix:
        config = getMapping(ex)
        configs.append(config)

    X = np.array(designMatrix, dtype=float)

    return configs, X

def getConfigs2():
    """
    Manually chosen
    """
    designMatrix = [
        [1,0,1,0,1,0],
        [1,0,1,0,0,1],
        [1,0,0,1,1,0],
        [1,0,0,1,0,1],
        [0,1,0,1,0,1],
        [0,1,0,1,1,0],
        [0,1,1,0,0,1],
        [0,1,1,0,1,0],
    ]
    X = np.array(designMatrix)
    x1x2 = X[:,0] * X[:,1]
    n,d = X.shape
    Xn = np.zeros((n,d+1))
    Xn[:,0:d] = X
    Xn[:,d] = x1x2

    configs = []
    for ex in designMatrix:
        config = getMapping(ex)
        configs.append(config)

    return configs, Xn



def experiment():
    random_seeds = [*range(settings.N_SAMPLES)]
    configs, X = getConfigs2()
    
    y = []
    for config in configs:
        samples = main.run_experiment(config, settings.N_SAMPLES, True, random_seeds)
        queue_length = (1 / len(samples)) * sum([sample["mean_queue_at_entrance"] for sample in samples])
        y.append(queue_length)
        
    y = np.array(y)

    model = RegressionModel()
    model.fit(X, y, verbose = False)
    print("beta", model.beta)
    print("mse", model.mse(X,y))
    print("r^2", model.r2(X,y))
    print("crossvalidation error", RegressionModel.crossValidate(X,y))

    prediction = model.predict([[0,0, 0,0,1,1]])
    config_for_test = {
        "interarrival_time_random_stream": exp(25),
        "preparation_time_random_stream": exp(40),
        "recovery_time_random_stream": exp(40),
        "n_preparation_rooms": 5,
        "n_recovery_rooms": 5,
        "cancelling_prob": settings.CANCELLING_PROBABILITY
    }
    samples = main.run_experiment(config, settings.N_SAMPLES, True, random_seeds)
    queue_length = (1 / len(samples)) * sum([sample["mean_queue_at_entrance"] for sample in samples])
    print("prediction", prediction)
    print("simulated", queue_length)

if __name__ == "__main__":
    experiment()