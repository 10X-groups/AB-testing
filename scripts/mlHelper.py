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
