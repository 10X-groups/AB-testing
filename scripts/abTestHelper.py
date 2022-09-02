"""
A script to help with AB hypothesis testing.
"""

from scipy.stats import norm
import math as mt
import logging


class abTestHelper():
    """
    The ab hypothesis helper class.
    """
    def __init__(self, fromThe: str) -> None:
        """
        The hypothesis test helper initializer

        Parameters
        =--------=
        fromThe: string
            The file importing the hypothesis test helper

        Returns
        =-----=
        None: nothing
            This will return nothing, it just sets up the Hypothesis test
            helper script.
        """
        try:
            # setting up logger
            self.logger = self.setup_logger('../logs/hypothesis_test_root.log')
            self.logger.info('\n    #####-->    AB hypothesis test logger for'
                             + f'{fromThe}    <--#####\n')
            print('Hypothesis test helper in action')
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

    def get_z_score(self, alpha):
        """
        A function to return z score based on given alpha value

        Parameters
        =--------=
        alpha: the alpha value on which z score is going to be calculated on

        Returns
        =-----=
        The z-score for given alpha
        """
        try:
            self.logger.info('calculating z score')
            z_score = norm.ppf(alpha)
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
            self.logger.info('z score calculated and returned')
            return z_score

    def get_std(self, p, total):
        """
        A function to return standard deviation

        Parameters
        =--------=
        p:  p value
        total: the total value

        Returns
        =-----=
        The standard deviation for given alpha total number and p value
        """
        try:
            self.logger.info('calculating standard deviation')
            std = mt.sqrt(p * (1-p) / (total))
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
            self.logger.info('standard deviation calculated and returned')
            return std

    def get_pooled_std(self, p_pooled, control_total, exposed_total):
        """
        A function to return pooled standard deviation

        Parameters
        =--------=
        p_pooled:  pooled p value
        control_total: the total value for the control data
        exposed_total: the total value for the exposed data

        Returns
        =-----=
        The pooled standard deviation for given input
        """
        try:
            self.logger.info('calculating pooled standard deviation')
            pooled_std = mt.sqrt(p_pooled * (1-p_pooled) *
                                 (1/control_total+1/exposed_total))
        except Exception as e:
            self.logger.error(e)
            print(e)
        finally:
            self.logger.info('pooled standard deviation calculated and' +
                             'returned')
            return pooled_std
