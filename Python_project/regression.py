import numpy as np
from sklearn import linear_model
from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score
from itertools import combinations

import main
import settings
import Hospital
from helpers import exp, unif


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

def add2Joints(X, excludeColumns):
    """
    Add nonlinear combinations of variables
    except for columns (i,j) in excludeColumns
    """   
    XT = X.T
    Xextended = []
    #add existing columns
    for row in XT:
        Xextended.append(row)

    for i in range(len(XT)):
        for j in range(i+1, len(XT)):
            if (i,j) not in excludeColumns:
                Xextended.append(XT[i] * XT[j])

    return np.array(Xextended).T
    

def getConfigs2(add_joint):
    """
    Manually chosen
    """
    designMatrix = settings.DESIGN_MATRIX
    X = np.array(designMatrix)
    if add_joint:
        X = add2Joints(X, settings.EXCLUDE_JOINTS)
    configs = []
    def transform(x):
        #-1 => 0, 1 => 1
        if x == -1:
            return 0
        return 1

    for ex in designMatrix:
        ex_01 = list(map(transform, ex))
        config = getMapping(ex_01)
        configs.append(config)

    return configs, X



def experiment(n_samples, add_joint, independent):
    """
    Run simulation and collect the simulated queue lengths
    fit linear regression model to simulation parameters and collected queue lengths
    predict for unseen example
    print information about the model
    Params:
        n_samples: int number of samples for each configurations
        add_joint: boolean whether to add 2 joint effects
        independent: boolean if true use same seed for each samples 
    """
    random_seeds = [*range(n_samples)]
    #configs, X = getConfigs()
    configs, X = getConfigs2(add_joint)

    #X_obs = np.empty(shape = (N_samp*len(configs), len(X[0])))
    X_obs = []
    y = []
    for i, config in enumerate(configs):
        samples = main.run_experiment(config, n_samples, independent, random_seeds)
        for j, sample in enumerate(samples):
            y.append(sample["mean_queue_at_entrance"])
            X_obs.append(X[i])

        #queue_length = (1 / len(samples)) * sum([sample["mean_queue_at_entrance"] for sample in samples])
        #y.append(queue_length)

    X_obs = np.array(X_obs)
    y = np.array(y)
    data = np.concatenate((X_obs, y.reshape(-1,1)), axis=1)
    #save to file
    np.savetxt("experiment_data.csv", data, delimiter=",")
        
    model = linear_model.LinearRegression(fit_intercept=True)
    #model = linear_model.Ridge(alpha=1, fit_intercept=True)
    model.fit(X_obs, y)

    #test model
    testX = np.array([settings.REGRESSION_TEST_X])
    if add_joint:
        testX = add2Joints(testX,settings.EXCLUDE_JOINTS)
    prediction = model.predict(testX)
    config_for_test = getMapping(testX[0])
    samples = main.run_experiment(config_for_test, n_samples, independent, random_seeds)
    actual = (1 / len(samples)) * sum([sample["mean_queue_at_entrance"] for sample in samples])

    printInformation(model, prediction, actual, X_obs, y)


def printInformation(model, prediction, actual, X, y):
    formatting = "{} {:.3f}"
    print("-"*20)
    print("REGRESSION")
    print("-"*20)
    with np.printoptions(precision=3):
        print("coefficients",model.coef_)

    print(formatting.format("intercept",model.intercept_))

    print(formatting.format("predicted", prediction[0]))
    print(formatting.format("simulated", actual))

    print(formatting.format("mean squared error", mean_squared_error(y, model.predict(X))))
    print(formatting.format("explained variance score", explained_variance_score(y, model.predict(X))))
    print(formatting.format("r^2 score", r2_score(y, model.predict(X))))
    print("-"*20)