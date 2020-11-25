import numpy as np

"""
Build a regression model for the average queue length. 
Which structural parameters affect the queue length significantly? 
Does the model make any sense (or are joint effects essential to take in to account in the model)?
"""

class RegressionModel:
    """
    Linear regression model
    """
    def __init__(self):
        self.w = None

    def fit(self, X, y):
        """
        Find optimal parameters
        Params:
            X: numpy ndarray (n, q)
            y: numpy ndarray (n,)
        Returns:
            least squared solution
        Raises: 
            LinAlgError("Singular matrix")
        """
        #@ is a general matrix multiplication / dot product operator in numpy
        self.w = np.linalg.inv(X.T @ X) @ X.T @ y
        return self.w

    def predict(self,x):
        """
        Evaluate model using calculated coefficients
        """
        return np.dot(self.w,x)


""" model = RegressionModel()

X = np.array([[1,2,3], [4,5,6], [6,7,2], [4,7,1]])

y = np.array([7, 19, 21, 16])

params = model.fit(X,y)

y_predicted = [model.predict(x) for x in X]
print("params",params)
print("actual",y)
print("predicted",y_predicted)
print("norm",np.linalg.norm(y - y_predicted)) """