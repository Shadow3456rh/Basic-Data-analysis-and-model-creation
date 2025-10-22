import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, r2_score, mean_squared_error, recall_score

def data_preprocessing(data, target):
    data=data.dropna()
    x = data.drop(target, axis=1)
    y= data[target]
    x_train, x_test, y_train, y_test=train_test_split(train_size=0.7, random_state=41)
    scaler = StandardScaler()
    x_train=scaler.fit_transform(x_train)
    x_test=scaler.transform(x_test)
    return x_train, x_test, y_train, y_test, scaler

def classification_algorithm(x_train, x_test, y_train, y_test):
    models=[GaussianNB(), RandomForestClassifier(), DecisionTreeClassifier()]
    results = []
    for i in models:
        model=i
        model.fit(x_train, y_train)
        pred=model.predict(x_test)
        accuracy = accuracy_score(y_test, pred)*100
        precision = precision_score(y_test, pred, average='weighted')*100
        recall = recall_score(y_test, pred,average='weighted')*100
        results.append({
            'model_name': model.__class__.__name__,
            'accuracy':accuracy,
            'precision':precision,
            'recall':recall,
            'pred':pred,
            'model_object':model
        })
    return results

def regression_algorithm(x_train, x_test, y_train, y_test):
    models = [RandomForestRegressor(), DecisionTreeRegressor(), LinearRegression(), LogisticRegression()]
    results=[]
    for i in models:
        model=i
        model.fit(x_train, y_train)
        pred=model.predict(x_test)
        mse = mean_squared_error(y_test, pred)
        r2 = r2_score(y_test, pred)
        results.append({
            'model_name': model.__class__.__name__,
            'MSE':mse,
            'R2':r2,
            'pred': pred,
            'model_object':model
        })
    return results