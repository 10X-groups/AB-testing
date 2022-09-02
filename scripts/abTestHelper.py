"""
A script to help with AB hypothesis testing.
"""

from scipy.stats import norm
import math as mt


class abTestHelper():
    """
    The ab hypothesis helper class.
    """
    def get_z_score(alpha):
        """
        A function to return z score based on given alpha value

        Parameters
        =--------=
        alpha: the alpha value on which z score is going to be calculated on

        Returns
        =-----=
        The z-score for given alpha
        """
        return norm.ppf(alpha)

    def get_std(p, total):
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
        return mt.sqrt(p * (1-p) / (total))

    def get_pooled_std(p_pooled, control_total, exposed_total):
        """
        A function to return pooled standard deviation

        Parameters
        =--------=
        p:  p value
        total: the total value

        Returns
        =-----=
        The spooled standard deviation for given input
        """
        return mt.sqrt(p_pooled * (1-p_pooled) *
                       (1/control_total+1/exposed_total))
