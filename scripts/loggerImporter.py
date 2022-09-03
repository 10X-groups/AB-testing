"""
A logger creator class.
"""

# imports
import logging


def setup_logger(log_path: str) -> logging.Logger:
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
