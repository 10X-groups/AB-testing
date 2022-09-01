"""
A script to clean data.
"""

# imports
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import logging

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
        try:
            # setting up logger
            self.logger = self.setup_logger('../logs/cleaner_root.log')
            self.logger.info(f'\n    #####-->    Data cleaner logger for {fromThe}    <--#####\n')
            print('Data cleaner in action')
        except Exception as e:
            print(e)

    def setup_logger(self, log_path: str) -> logging.Logger:
        """
        A function to set up logging

        Parameters
        =--------=
        log_path: string
            The path of the file handler for the logger

        Returns
        =-----=
        logger: logger
            The final logger that has been setup up
        """
        try:
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
        except Exception as e:
            logger.error(e)
            print(e)
        finally:
            return logger

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
            self.logger.info(f'columns: {cols} removed successfully')
        except Exception as e:
            self.logger.error(e)
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
            self.logger.info("The dataset contains", round((
                                                (totalMissing/totalCells)*100
                                                ),10), "%", "missing values")
        except Exception as e:
            self.logger.error(e)
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
            self.logger.info(f"features start and end successfully converted"
                               + "to date time")
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
            return df

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
            self.logger.info(f'cols: {cols} filled with median successfully')
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
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
            self.logger.info(f'cols: {cols} filled with mean successfully')
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
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
            self.logger.info(f'column: {column} outlier fixed successfully')
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
            return df[column]

    # TODO  : determine which one is better
    def fix_outlier_(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A function to fix outliers

        Parameters
        =--------=
        df:  pandas data frame
            The data frame containing the outlier columns

        Returns
        =-----=
        df:  pandas data frame
            The data frame with the outlier columns fixed
        """
        try:
            self.logger.info(f'setting up columns to be fixed for outlier')
            # TODO : either pass the outlier columns or checkout the columns list 
            column_name=list(df.columns[2:])
            for i in column_name:
                upper_quartile=df[i].quantile(0.75)
                lower_quartile=df[i].quantile(0.25)
                df[i]=np.where(df[i]>upper_quartile,df[i].median(),
                            np.where(df[i]<lower_quartile,df[i].median(),
                            df[i]))
            self.logger.info(f'outliers fixed successfully')
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
            return df

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
            self.logger.info(f'distortion: {distortions} and inertia:' +  
                             f'{inertias} calculated for {num} number of'
                              'clusters successfully')
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
            return (distortions, inertias)

    def computeBasicAnalysisOnClusters(self, df: pd.DataFrame, 
                                       cluster_col: str , cluster_size: int,
                                       cols: list) -> None:
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
        try:
            i=0
            for i in range(cluster_size):
                cluster = df[df[cluster_col]==i]
                print("Cluster " + (i+1) * "I")
                print(cluster[cols].describe())
                print("\n")
            self.logger.info(f'basic analysis on {cluster_size} clusters' + 
                              'computed successfully')
        except Exception as e:
            self.logger.error(e)
            print(e)
