import numpy as np
from sklearn import linear_model
from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score

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
    """ x1x2 = X[:,0] * X[:,1]
    n,d = X.shape
    Xn = np.zeros((n,d+1))
    Xn[:,0:d] = X
    Xn[:,d] = x1x2 """

    configs = []
    for ex in designMatrix:
        config = getMapping(ex)
        configs.append(config)

    return configs, X



def experiment():
    """
    Run simulation and collect the simulated queue lengths
    fit linear regression model to simulation parameters and collected queue lengths
    predict for unseen example
    print information about the model
    """
    random_seeds = [*range(settings.N_SAMPLES)]
    configs, X = getConfigs2()
    independent = True

    N_samp = 10
    X_obs = np.empty(shape = (N_samp*len(configs), len(X[0])))
    y = np.array([])
    for i, config in enumerate(configs):
        samples = main.run_experiment(config, N_samp, independent, random_seeds)
        for j, sample in enumerate(samples):
            y = np.append(y, sample["mean_queue_at_entrance"])
            X_obs[i*len(samples) + j] = X[i]
        #queue_length = (1 / len(samples)) * sum([sample["mean_queue_at_entrance"] for sample in samples])
        #y.append(queue_length)

    data = np.concatenate((X_obs, np.array([y]).T), axis=1)

    #save to file
    np.savetxt("experiment_data.csv", data, delimiter=",")
        
    y = np.array(y)
    model = linear_model.LinearRegression(fit_intercept=True)
    model.fit(X_obs, y)
    
    testX = [0,0,0,0,1,1]
    prediction = model.predict([testX])
    config_for_test = getMapping([0,0,0,0,1,1])
    samples = main.run_experiment(config_for_test, N_samp, independent, random_seeds)
    queue_length = (1 / len(samples)) * sum([sample["mean_queue_at_entrance"] for sample in samples])

    formatting = "{} {:.3f}"
    print("-"*20)
    print("REGRESSION")
    print("-"*20)
    with np.printoptions(precision=2):
        print("coefficients",model.coef_)
        print("intercept",model.intercept_)

    print(formatting.format("prediction", prediction[0]))
    print(formatting.format("simulated", queue_length))

    print(formatting.format("mean squared error", mean_squared_error(y, model.predict(X_obs))))
    print(formatting.format("explained variance score", explained_variance_score(y, model.predict(X_obs))))
    print(formatting.format("r^2 score", r2_score(y, model.predict(X_obs))))
    print("-"*20)

