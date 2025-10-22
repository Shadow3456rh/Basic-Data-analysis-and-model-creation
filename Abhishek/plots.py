import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df =None

def load_dataset(data):
    global df
    try:
        df.read_csv(data)
        print("Dataset loaded successfully: ")
        return df
    except Exception as e:
        print("Error dataset")
        return None 



def scatterplot(x, y):
    global df
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y], color="red")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"{x} vs {y}")
    return fig

def histogram():
    global df
    fig, ax = plt.subplots()
    df.hist(ax=ax)
    ax.set_title("Histogram")
    return fig

def corr_heatmap():
    global df
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", ax=ax)
    ax.set_title("Correlation Heatmap")
    return fig

def pair_plots():
    global df
    fig = sns.pairplot(df)
    fig.fig.suptitle("Pair Plot", y=1.02)
    return fig.fig  

def line_plot(test, pred):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(test, pred, color="blue", label="Test data")
    ax.plot([test.min(), test.max()], [test.min(), test.max()], color='red', lw=2, label='Perfect fit')
    ax.legend()
    ax.grid(True)
    ax.set_title("Line Plot")
    return fig
