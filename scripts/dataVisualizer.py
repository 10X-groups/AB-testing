"""
A script to visualize data.
"""

# imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from loggerImporter import setup_logger
import logging

class dataVisualizer():
    """
    A data visulalizer class.
    """
    def __init__(self, fromThe: str) -> None:
        """
        The data visualizer initializer

        Parameters
        =--------=
        fromThe: string
            The file importing the data visualizer

        Returns
        =-----=
        None: nothing
            This will return nothing, it just sets up the data visualizer
            script.
        """
        self.logger = self.setup_logger('../logs/visualizer_root.log')
        self.logger.info(f'data visualier logger for {fromThe}.')
        print('Data visualizer in action')

    def setup_logger(self, log_path: str) -> logging.Logger:
        """
        A helper method to set up logging.

        Parameters
        =--------=
        log_path: a python string object
            The path of the file handler for the logger

        Returns
        =-----=
        logger: a python logger object
            The final logger that has been setup up
        """
        # getting the log path
        log_path = log_path

        # adding logger to the script
        logger = logging.getLogger(__name__)
        print(f'--> {logger}')
        # setting the log level to info
        logger.setLevel(logging.INFO)
        # setting up file handler
        file_handler= logging.FileHandler(log_path)

        # setting up formatter
        formatter= logging.Formatter(
            "%(levelname)s : %(asctime)s : %(name)s : %(funcName)s " + 
            "--> %(message)s")

        # setting up file handler and formatter
        file_handler.setFormatter(formatter)
        # adding file handler
        logger.addHandler(file_handler)

        print(f'logger {logger} created at path: {log_path}')
        # return the logger object
        return logger

    def plot_pie(self, df: pd.DataFrame, column: str, title: str,
                 largest:int = 10) -> None:
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
        self.logger.info(f'{title} pie plot ploted successfully')

    def plot_hist(self, df: pd.DataFrame, column: str, color: str) -> None:
        # plt.figure(figsize=(15, 10))
        # fig, ax = plt.subplots(1, figsize=(12, 7))
        self.logger.info(f'setting up distribution plot')
        sns.displot(data=df, x=column, color=color, kde=True, height=7,
                    aspect=2)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()
        # TODO: if logger info is bad try this
        # logger.info(f'Distribution of {column} plot successfully plotted')
        self.logger.info(f'{plt.title} hist plot ploted successfully')

    def plot_count(self, df: pd.DataFrame, column: str) -> None:
        self.logger.info(f'setting up count plot')
        plt.figure(figsize=(12, 7))
        # TODO: get edegcolor meaning and add color
        sns.countplot(data=df, x=column, facecolor=(0, 0, 0, 0), linewidth=5,  edgecolor=sns.color_palette("pastel", 3))
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.xlabel(f'{column}', fontsize=16)
        plt.ylabel("Count", fontsize=16)
        plt.show()
        # TODO: if logger info is bad try this
        # logger.info(f'Distribution of {column} plot successfully plotted')
        self.logger.info(f'{plt.title} count plot ploted successfully')

    def plot_bar(self, df: pd.DataFrame, x_col: str, y_col: str, title: str,
                 xlabel: str, ylabel: str) -> None:
        self.logger.info(f'setting up bar plot')
        plt.figure(figsize=(12, 7))
        # TODO: modify palette
        sns.barplot(data=df, x=x_col, y=y_col, palette= "Blues")
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.show()
        self.logger.info(f'{title} bar plot ploted successfully')

    def plot_heatmap(self, df: pd.DataFrame, title: str, cbar=False) -> None:
        self.logger.info(f'setting up heat map plot')
        plt.figure(figsize=(12, 7))
        sns.heatmap(df, annot=True, cmap='viridis', vmin=0, vmax=1, fmt='.2f',
                    linewidths=.7, cbar=cbar)
        plt.title(title, size=20, fontweight='bold')
        plt.show()
        self.logger.info(f'{title} heat map plot ploted successfully')

    def plot_box(self, df: pd.DataFrame, x_col: str, title: str) -> None:
        self.logger.info(f'setting up box plot')
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.show()
        self.logger.info(f'{title} box plot ploted successfully')

    def plot_box_multi(self, df: pd.DataFrame, x_col: str, y_col: str,
                       title: str) -> None:
        self.logger.info(f'setting up box plot')
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
        self.logger.info(f'{title} multi box plot ploted successfully')

    def plot_scatter(self, df: pd.DataFrame, x_col: str, y_col: str, title: str,
                     hue: str, style: str) -> None:
        self.logger.info(f'setting up scatter plot')
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue, style=style)
        plt.title(title, size=20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
        self.logger.info(f'{title} scatter plot ploted successfully')

    def bivariate_plot(self, df,features, fields):
        fig, axs = plt.subplots(10,3, figsize=(20,45))
        for col in range(len(features)):  
            for f in range(len(fields)):  
                self.logger.info(f'setting up hist plot')
                sns.histplot(df, 
                            x=features[col]+"_"+fields[f], 
                            hue="diagnosis", element="bars", 
                            stat="count", 
                            # TODO : modify palette
                            palette=["gold", "purple"],
                            ax=axs[col][f])
        self.logger.info(f'several bi-variate plots plotted successfully')
