"""
A script for machine learning preprocessing.
"""

# imports
import pandas as pd
from sklearn import preprocessing
import logging

class machineLearningHelper():
    """
    A data preprocessing class for machine learning.
    """
    def __init__(self, fromThe: str) -> None:
        """
        The data preprocessing initializer

        Parameters
        =--------=
        fromThe: string
            The file importing the data preprocessor

        Returns
        =-----=
        None: nothing
            This will return nothing, it just sets up the data preprocessing
            script.
        """
        try:
            # setting up logger
            self.logger = self.setup_logger('../logs/ml_preprocess_root.log')
            self.logger.info('\n    #####-->    Data preprocessing logger for ' +
                             f'{fromThe}    <--#####\n')
            print('Data preprocessor in action')
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
            file_handler = logging.FileHandler(log_path)

            # setting up formatter
            formatter = logging.Formatter(
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

    def print_result (self, model_result : dict, scoring_metrics : list,
                      metrics_type : str) -> None:
        """
        A function for creating model result reports: Mean

        Parameters
        =--------=
        model_result: dict
            Result of the model
        scoring_metrics: list
            List of scoring metrics
        metrics_type: str
            string of the metics type

        Returns
        =-----=
        None: nothing
            It will only print out the results
        """
        if metrics_type == 'mean':
            print('\n--- Mean Report ---')
            self.logger.info('setting up mean report')
            print(f"fit time: {round(model_result['fit_time'].mean(), 4)}")
            self.logger.info(f"fit time: {round(model_result['fit_time'].mean(), 4)}")
            print(f"score time: {round(model_result['score_time'].mean(), 4)}")
            self.logger.info(f"score time: {round(model_result['score_time'].mean(), 4)}")
            for scores in scoring_metrics:
                #train_key = 'train_' + scores
                test_key = 'test_' + scores
                #print(f"{train_key}: {round(model_result[train_key].mean(), 4)}")
                print(f"{test_key}: {round(model_result[test_key].mean(), 4)}")
                self.logger.info(f"{test_key}: {round(model_result[test_key].mean(), 4)}")
        
        if metrics_type == 'std':
            print('\n--- Standard deviation Report ---')
            self.logger.info('setting up standard deviation report')
            print(f"fit time: {round(model_result['fit_time'].std(), 4)}")
            self.logger.info(f"fit time: {round(model_result['fit_time'].std(), 4)}")
            print(f"score time: {round(model_result['score_time'].std(), 4)}")
            self.logger.info(f"score time: {round(model_result['score_time'].std(), 4)}")
            for scores in scoring_metrics:
                #train_key = 'train_' + scores
                test_key = 'test_' + scores
                #print(f"{train_key}: {round(model_result[train_key].std(), 4)}")
                print(f"{test_key}: {round(model_result[test_key].std(), 4)}")
                self.logger.info(f"{test_key}: {round(model_result[test_key].std(), 4)}")
