"""
A script to visualize data
"""

# imports
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class dataVisualizer():
    def __init__(self) -> None:
        print('Data visualizer in action.')

    def plot_pie(self, df: pd.DataFrame, column: str, title: str, largest:int = 10) -> None:
        """
        A function to plot pie charts

        Parameters
        =--------=

        Returns
        =-----=
        None: nothing
            Only plots the plot
        """
        fig = plt.figure(figsize=(10, 10))
        col = df[column].value_counts().nlargest(n=largest)

        data = col.values
        labels = col.keys()

        last_num = len(data)

        colors = sns.color_palette('muted')[0:last_num]

        plt.pie(data, labels=labels, colors=colors, autopct='%.000f%%')
        plt.title(title)
        plt.show()

    def plot_hist(df: pd.DataFrame, column: str, color: str) -> None:
        # plt.figure(figsize=(15, 10))
        # fig, ax = plt.subplots(1, figsize=(12, 7))
        sns.displot(data=df, x=column, color=color, kde=True, height=7,
                    aspect=2)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()

    def plot_count(df: pd.DataFrame, column: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.countplot(data=df, x=column)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()

    def plot_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str,
                 xlabel: str, ylabel: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.barplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.show()

    def plot_heatmap(df: pd.DataFrame, title: str, cbar=False) -> None:
        plt.figure(figsize=(12, 7))
        sns.heatmap(df, annot=True, cmap='viridis', vmin=0, vmax=1, fmt='.2f',
                    linewidths=.7, cbar=cbar)
        plt.title(title, size=18, fontweight='bold')
        plt.show()

    def plot_box(df: pd.DataFrame, x_col: str, title: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.show()

    def plot_box_multi(df: pd.DataFrame, x_col: str, y_col: str,
                       title: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()

    def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str, title: str,
                     hue: str, style: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue, style=style)
        plt.title(title, size=20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
