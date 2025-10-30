import pandas as pd
from sklearn.datasets import load_iris

from modeltraining import (classification_algorithm, data_preprocessing,
                           regression_algorithm)

iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)
data["target"] = iris.target


x_train, x_test, y_train, y_test, scaler = data_preprocessing(data, "target")
results = classification_algorithm(x_train, x_test, y_train, y_test)
print(results)
reg_results = regression_algorithm(x_train, x_test, y_train, y_test)
print(reg_results)
