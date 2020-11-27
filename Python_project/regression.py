import numpy as np

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
            print(self)
        return self.beta

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
            s = str({
            "beta": self.beta,
            "mse": self.mse(X,y),
            "R^2": self.r2(X,y)
        })
        return s 



if __name__ == "__main__":
    import matplotlib.pyplot as plt

    model = RegressionModel()

    n = 100
    x1 = np.random.exponential(scale=10, size=n)
    x2 = np.random.exponential(scale=20, size=n)
    x3 = np.random.normal(0, 4, size=n)
    x4 = np.random.normal(4, 5, size=n)
    #y = x1 + 2 * x2 + 100
    y = 2 * x1 - 3 * x2 + x3 + 15
    #y = 2 * x1 

    X = np.column_stack((x1, x2, x4)) 

    params = model.fit(X,y, verbose=False)
    y_predicted = model.predict(X)
    print(model)
    #print("params",params)
    #print("mse",model.mse(X,y))
    #print("r2", model.r2(X,y))
    
    plt.rcParams["legend.fontsize"] = 10

    fig = plt.figure()
    ax = fig.gca(projection="3d")

    ax.scatter(x1, x2, y_predicted, label='predicted' + str(params))
    ax.scatter(x1, x2, y, label='actual')
    ax.legend()

    plt.show()