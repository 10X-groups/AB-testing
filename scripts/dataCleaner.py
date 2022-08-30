"""
A script to clean data.
"""

# imports
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from logger_importer import setup_logger


class dataCleaner():
    """
    A data cleaner class.
    """
    def __init__(self, fromThe: str) -> None:
        """
        The data cleaner initializer

        Parameters
        =--------=
        fromThe: string
            The file importing the data cleaner

        Returns
        =-----=
        None: nothing
            This will return nothing, it just sets up the data cleaner
            script.
        """
        logger= setup_logger('../logs/cleaner_root.log')
        logger.info(f'created a data cleaner logger for {fromThe}.')
        print('Data cleaner in action.')

    def remove_unwanted_cols(self, cols: list) -> pd.DataFrame:
        """
        A function to remove unwanted columns from a DataFrame

        Parameters
        =--------=
        cols: list
            The unwanted column lists

        Returns
        =-----=
        self.df
            The dataframe rid of the unwanted cols
        """
        try:
            self.df.drop(cols, axis=1, inplace=True)
        except Exception as e:
            print(e)
        finally:
            return self.df

    def percent_missing(self, df: pd.DataFrame) -> None:
        """
        A function telling how many missing values exist or better still
        what is the % of missing values in the dataset?

        Parameters
        =--------=
        df: pandas dataframe
            The data frame to calculate the missing values from

        Returns
        =-----=
        None: nothing
            Just prints the missing value percentage
        """
        try:
            # Calculate total number of cells in dataframe
            totalCells = np.product(df.shape)

            # Count number of missing values per column
            missingCount = df.isnull().sum()

            # Calculate total number of missing values
            totalMissing = missingCount.sum()

            # Calculate percentage of missing values
            print("The dataset contains", round(((totalMissing/totalCells)*
                                                 100), 10), "%", 
                                                 "missing values.")
        except Exception as e:
            print(e)

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A function to convert datetime column to datetime

        Parameters
        =--------=
        df: pandas data frame
            The data frame to modify

        Returns
        =-----=
        df: pandas dataframe
            The modified dataframe
        """
        try:
            df['Start'] = pd.to_datetime(df['Start'], errors='coerce')
            df['End'] = pd.to_datetime(df['End'], errors='coerce')
        except Exception as e:
            print(e)
        return df

    def fill_na(self, type: str, df: pd.DataFrame, 
                cols: list) -> pd.DataFrame:
        """
        A function to fill nulls and undefined data types

        Parameters
        =--------=
        type: string
            The type of the fill. Eg: mode, mean, median
        df: pd.dataframe
            The data frame to fill
        cols: list
            The list of columns to be filled

        Returns
        =-----=
        self.df: pandas dataframe
            The modified dataframe
        """
        try:
            if (type == 'mean'):
                for col in cols:
                    self.df.col.fillna(value=df.col.mean(), axis=1,
                                    inplace=True)
                return self.df
            elif (type == 'median'):
                for col in cols:
                    self.df.col.fillna(value=df.col.median(), axis=1,
                                    inplace=True)
                return self.df
            elif (type == 'mode'):
                for col in cols:
                    self.df.col.fillna(value=df.col.mode(), axis=1,
                                    inplace=True)
                return self.df
            else:
                print('type must be either mean, median or mode')
        except Exception as e:
            print(e)

    def fillWithMedian(self, df: pd.DataFrame, cols: list) -> pd.DataFrame:
        """
        A function that fills null values with their corresponding median 
        values

        Parameters
        =--------=
        df: pandas data frame
            The data frame with the null values
        cols: list
            The list of columns to be filled with median values

        Returns
        =-----=
        df: pandas data frame
            The data frame with the null values replace with their
            corresponding median values
        """
        try:
            print(f'columns to be filled with median values: {cols}')
            df[cols] = df[cols].fillna(df[cols].median())
        except Exception as e:
            print(e)
        return df

    def fillWithMean(self, df: pd.DataFrame, cols: list) -> pd.DataFrame:
        """
        A function that fills null values with their corresponding mean 
        values

        Parameters
        =--------=
        df: pandas data frame
            The data frame with the null values
        cols: list
            The list of columns to be filled with mean values

        Returns
        =-----=
        df: pandas data frame
            The data frame with the null values replace with their
            corresponding mean values
        """
        try:
            print(f'columns to be filled with mean values: {cols}')
            df[cols] = df[cols].fillna(df[cols].mean())
        except Exception as e:
            print(e)
        return df

    def fix_outlier(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        A function to fix outliers with median

        Parameters
        =--------=
        df: pandas data frame
            The data frame containing the outlier columns
        column: str
            The string name of the column with the outlier problem 

        Returns
        =-----=
        df: pandas data frame
            The fixed data frame
        """
        try:
            print(f'column to be filled with median values: {column}')
            df[column] = np.where(df[column] > df[column].quantile(0.95),
                                df[column].median(),df[column])
        except Exception as e:
            print(e)
        return df[column]

    def choose_k_means(self, df: pd.DataFrame, num: int):
        """
        A function to choose the optimal k means cluster

        Parameters
        =--------=
        df: pandas data frame
            The data frame that holds all the values
        num: integer
            The x scale

        Returns
        =-----=
        distortions and inertias
        """
        try:
            distortions = []
            inertias = []
            K = range(1, num)
            for k in K:
                k_means = KMeans(n_clusters=k, random_state=777).fit(df)
                distortions.append(sum(
                    np.min(cdist(df, k_means.cluster_centers_, 'euclidean'), 
                                axis=1)) / df.shape[0])
                inertias.append(k_means.inertia_)
        except Exception as e:
            print(e)

        return (distortions, inertias)

    def computeBasicAnalysisOnClusters(self, df: pd.DataFrame, 
                                       cluster_col: str , cluster_size: int,
                                       cols: list):
        """
        A function that gives some basic description of the 3 clusters
        
        Parameters
        =--------=
        df: pandas data frame
            The main data frame containing all the data
        cluster_col: str
            The column name holding the cluster values
        cluster_size: integer
            The number of total cluster groups
        cols: list
            The column list on which to provide description

        Returns
        =-----=
        None: nothing
            This function only prints out information
        """
        i=0
        try:
            for i in range(cluster_size):
                cluster = df[df[cluster_col]==i]
                print("Cluster " + (i+1) * "I")
                print(cluster[cols].describe())
                print("\n")
        except Exception as e:
            print(e)
