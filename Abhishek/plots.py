import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = None


def load_dataset(data):
    global df
    try:
        df = pd.read_csv(data)
        print("✅ Dataset loaded successfully")
        return df
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return df


def scatterplot(x, y):
    global df
    if df is None:
        print("⚠️ Dataset not loaded.")
        return
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y], color="red")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"{x} vs {y}")
    plt.show()
    return fig


def histogram():
    global df
    if df is None:
        print("⚠️ Dataset not loaded.")
        return
    df.hist(figsize=(10, 6))
    plt.suptitle("Histogram")
    plt.show()


def corr_heatmap():
    global df
    if df is None:
        print("⚠️ Dataset not loaded.")
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", ax=ax)
    ax.set_title("Correlation Heatmap")
    plt.show()
    return fig


def pair_plots():
    global df
    if df is None:
        print("⚠️ Dataset not loaded.")
        return
    fig = sns.pairplot(df)
    fig.fig.suptitle("Pair Plot", y=1.02)
    plt.show()
    return fig.fig


def line_plot(test, pred):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(test, pred, color="blue", label="Test data")
    ax.plot(
        [test.min(), test.max()],
        [test.min(), test.max()],
        color="red",
        lw=2,
        label="Perfect fit",
    )
    ax.legend()
    ax.grid(True)
    ax.set_title("Line Plot")
    plt.show()
    return fig


# file = open("./Ice Cream.csv")
# load_dataset(file)
# pair_plots()
