"""
A script to help with AB hypothesis testing.
"""

import random
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
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
        =---------=
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
            self.logger.info('\n    #####-->    AB hypothesis test logger for '
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

    def transform_data(self, df):
        '''
        segment data into exposed and control groups
        consider that SmartAd runs the experiment hourly, group data into hours. 
            Hint: create new column to hold date+hour and use df.column.map(lambda x:  pd.Timestamp(x,tz=None).strftime('%Y-%m-%d:%H'))
        create two data frame with bernoulli series 1 for positive(yes) and 0 for negative(no)
            Hint: Given engagement(sum of yes and no until current observation as an array) and success (yes count as an array), the method generates random binomial distribution
                #Example
                engagement = np.array([5, 3, 3])
                yes = np.array([2, 0, 3])
                Output is "[1] 1 0 1 0 0 0 0 0 1 1 1", showing a binary array of 5+3+3 values
                of which 2 of the first 5 are ones, 0 of the next 3 are ones, and all 3 of
                the last 3 are ones where position the ones is randomly distributed within each group.
        '''

        def get_bernoulli_series(engagement_list, success_list):
            bernoulli_series = []

            self.logger.info('preparing bernoulli series')
            for engagement, success in zip(engagement_list, success_list):
                no_list = (engagement - success) * [0]
                yes_list = (success) * [1]
                series_item = yes_list + no_list
                random.shuffle(series_item)
                bernoulli_series += series_item
            self.logger.info('returning bernoulli series')
            return np.array(bernoulli_series)

        clean_df = df.query("not (yes == 0 & no == 0)")

        exposed = clean_df[clean_df['experiment'] == 'exposed']
        control = clean_df[clean_df['experiment'] == 'control']

        # group data into hours.
        control['hour'] = control['hour'].astype('str')
        control['date_hour'] = pd.to_datetime(control['date'] + " " + control['hour'] + ":00:00")
        control['date_hour'] = control['date_hour'].map(lambda x:  pd.Timestamp(x, tz=None).strftime('%Y-%m-%d:%H'))

        exposed['hour'] = exposed['hour'].astype('str')
        exposed['date_hour'] = pd.to_datetime( exposed['date'] + " " + exposed['hour'] + ":00:00")
        exposed['date_hour'] = exposed['date_hour'].map( lambda x:  pd.Timestamp(x, tz=None).strftime('%Y-%m-%d:%H'))

        # create two data frame with bernoulli series 1 for positive(yes) and 0 for negative(no)
        self.logger.info('preparing control group bernoulli series')
        cont = exposed.groupby('date_hour').agg({'yes': 'sum', 'no': 'count'})
        cont = cont.rename(columns={'no': 'total'})
        control_bernoulli = get_bernoulli_series(
            cont['total'].to_list(), cont['yes'].to_list())

        self.logger.info('preparing exposed group bernoulli series')
        exp = exposed.groupby('date_hour').agg({'yes': 'sum', 'no': 'count'})
        exp = exp.rename(columns={'no': 'total'})
        exposed_bernoulli = get_bernoulli_series(
            exp['total'].to_list(), exp['yes'].to_list())

        self.logger.info('returning control and exposed group bernoulli series')
        return control_bernoulli, exposed_bernoulli

    def conditionalSPRT(self, x,y,t1,alpha=0.05,beta=0.10,stop=None):
        """
        #
        # Meeker's SPRT for matched `x` (treatment) and `y` (control), 
        # both indicator responses, likelihood ratio t1, error rates alpha and beta,
        # and (optionally) truncation after trial stop.
        #
        # The return variable contains these elements:
        #(outcome,n, k,l,u,truncated,truncate_decision,x1,r,stats,limits)
        # * outcome:   "continue," "reject null," or "accept null".
        # * n: number observation used for the decision
        # * k:     Index at which the outcome decision was made (or NA)
        # * l:     lower critical point
        # * u:     upper critical point
        # * truncate_decision: The approximate decision made after truncate point
        # * truncated: If the test was truncated, the value of `n.0`; NA otherwise
        # * x1:       Original data `x`, cumulative
        # * r:         Cumulative sum of x+y
        # * stats:     Series of cumulative sums of log probability ratios
        # * limits:    Two rows giving lower and upper critical limits, respectively
        #
        """
        if t1<=1:
            print('warning',"Odd ratio should exceed 1.")
            # self.logger.warn("Odd ratio should exceed 1.")
        if (alpha >0.5) | (beta >0.5):
            print('warning',"Unrealistic values of alpha or beta were passed."
                        +" You should have good reason to use large alpha & beta values")
            # self.logger.warn("Unrealistic values of alpha or beta were passed."
                        # +" You should have good reason to use large alpha & beta values")
        if stop!=None:
            stop=math.floor(n0)

        def comb(n, k):
            return math.factorial(n) // math.factorial(k) // math.factorial(n - k)

        def l_choose(b, j):
            a=[]
            if (type(j) is list) | (isinstance(j,np.ndarray)==True):
                if len(j)<2:
                    j=j[0]
            if (type(j) is list) | (isinstance(j,np.ndarray)==True):
                for k in j:
                    n=b
                    if (0 <= k) & (k<= n):
                        a.append(math.log(comb(n,k)))
                    else:
                        a.append(0)
            else:
                n=b
                k=j
                if (0 <= k) & (k<= n):
                    a.append(math.log(comb(n,k)))
                else:
                    a.append(0)

            return np.array(a)

        def g(x,r,n,t1,t0=1):
            """
            #
            # Meeker's (1981) function `g`, the log probability ratio.
            # 
            """
            return -math.log(h(x,r,n,t1))+math.log(h(x,r,n,t0))

        def h(x,r,n,t=1):
            """
            #
            # Reciprocal of Meeker's (1981) function `h`: the conditional probability of 
            # `x` given `r` and `n`, when the odds ratio is `t`.
            #
            # `x` is his "x1", the number of positives in `n` control trials.
            # `r` is the total number of positives.
            # `n` is the number of (control, treatment) pairs.
            # `t` is the odds ratio.
            #
            """
            return f(r,n,t,offset=ftermlog(x,r,n,t))

        def f(r,n,t,offset=0):
            """#
            # Meeker's (1981) function exp(F(r,n,t)), proportional to the probability of 
            #  `r` (=x1+x2) in `n` paired trials with an odds ratio of `t`.
            #
            # This function does *not* vectorized over its arguments.
            #"""
            upper=max(0,r-n)
            lower=min(n,r)
            rng=list(range(upper,lower+1))
            return np.sum(fterm(rng,r,n,t,offset))

        def fterm(j,r,n,t,offset=0):
            ft_log=ftermlog(j,r,n,t,offset)
            return np.array([math.exp(ex) for ex in ft_log])

        def ftermlog(j,r,n,t,offset=0):
            """
            #
            # Up to an additive constant, the log probability that (x1, x1+x2) = (j, r) 
            # in `n` paired trials with odds ratio of `t`.
            #
            # `offset` is used to adjust the result to avoid under/overflow.
            #
            """
            xx=r-j
            lch=l_choose(n,j)
            lchdiff=l_choose(n,xx)
            lg=np.array(j)*math.log(t)
            lgsum=lch+lchdiff
            lgsum2=lgsum+lg
            lgdiff=lgsum2-offset

            return lgdiff

        def logf(r,n,t,offset=0):
            """
            #
            # A protected vesion of log(f), Meeker's function `F`.
            #
            """
            z=f(r,n,t,offset)
            if z>0:
                return math.log(z)
            else:
                return np.nan

        def clowerUpper(r,n,t1c,t0=1,alpha=0.05,beta=0.10):
            """
            #
            # Meeker's (1981) functions c_L(r,n) and c_U(r,n), the  critical values for x1.
            # 0 <= r <= 2n; t1 >= t0 > 0.
            #
            """
            offset=ftermlog(math.ceil(r/2),r,n,t1c)
            z=logf(r,n,t1c,logf(r,n,t0,offset)+offset)
            a=-math.log(alpha/(1-beta))
            b=math.log(beta/(1-alpha))
            lower=b
            upper=1+a
            return (np.array([lower,upper])+z)/math.log(t1c/t0)

        l=math.log(beta/(1-alpha))
        u=-math.log(alpha/(1-beta))
        sample_size=min(len(x),len(y))
        n=np.array(range(1,sample_size+1))

        if stop!=None:
            n=np.array([z for z in n if z<=stop])
        x1=np.cumsum(x[n-1])
        r=x1+np.cumsum(y[n-1])
        stats=np.array(list(map(g,x1, r, n, [t1]*len(x1)))) #recursively calls g
            #
            # Perform the test by finding the first index, if any, at which `stats`
            # falls outside the open interval (l, u).
            #
        clu=list(map(clowerUpper,r,n,[t1]*len(r),[1]*len(r),[alpha]*len(r), [beta]*len(r)))
        limits=[]
        for v in clu:
            inArray=[]
            for vin in v:
                inArray.append(math.floor(vin))
            limits.append(np.array(inArray))
        limits=np.array(limits)

        k=np.where((stats>=u) | (stats<=l))
        c_values=stats[k]
        if c_values.shape[0]<1:
            k= np.nan
            outcome='Unable to conclude.Needs more sample.'
        else:
            k=np.min(k)
            if stats[k]>=u:
                outcome=f'Exposed group produced a statistically significant increase.'
            else:
                outcome='Their is no statistically significant difference between two test groups'
        if (stop!=None) & (k==np.nan):
            #
            # Truncate at trial stop, using Meeker's H0-conservative formula (2.2).
            # Leave k=NA to indicate the decision was made due to truncation.
            #
            c1=clowerUpper(r,stop,t1,alpha,beta)
            c1=math.floor(np.mean(c1)-0.5)
            if x1[n0]<=c1:
                truncate_decision='h0'
                outcome='Maximum Limit Decision. The aproximate decision point shows their is no statistically significant difference between two test groups'
            else:
                truncate_decision='h1'
                outcome=f'Maximum Limit Decision. The aproximate decision point shows exposed group produced a statistically significant increase.'
            truncated=stop
        else:
            truncate_decision='Non'
            truncated=np.nan
        return (outcome,n, k,l,u,truncated,truncate_decision,x1,r,stats,limits)


class ConditionalSPRT():
    #REFERENCE
    # A Conditional Sequential Test for the Equality of Two Binomial Proportions
    # William Q. Meeker, Jr
    # Journal of the Royal Statistical Society. Series C (Applied Statistics)
    # Vol. 30, No. 2 (1981), pp. 109-115
    def __init__(self, exposed, control, odd_ratio, alpha=0.05, beta=0.10, stop=None):
        self.exposed = exposed
        self.control = control
        self.odd_ratio = odd_ratio
        self.alpha = alpha
        self.beta = beta
        self.stop = stop

    def run(self):
        res = abTestHelper.conditionalSPRT( self.exposed,
                               self.control,
                               self.odd_ratio,
                               self.alpha,
                               self.beta,
                               self.stop)
        return res

    def jsonResult(self, res):
        outcome,n, k,l,u,truncated,truncate_decision,x1,r,stats,limits = res
        res = {
            "decisionMade": outcome,
            "numberOfObservation": len(n),
            "truncated": truncated,
            "truncateDecision": truncate_decision
        }
        return res

    def plotExperiment(self, res):
        outcome,n, k,l,u,truncated,truncate_decision,x1,r,stats,limits = res
        lower = limits[:, 0]
        upper = limits[:,1]

        fig, ax = plt.subplots(figsize=(12,7))
        ax.plot(n, x1, label='Cumulative value of yes+no')

        ax.plot(n, lower, label='Lower Bound')
        ax.plot(n, upper, label='Upper Bound')

        plt.legend()
        plt.show()
