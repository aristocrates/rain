"""
Get the probability that it is actually raining in Seattle.

Given that n friends in Seattle each lie with probability p, and each say
that it is raining, the probability that it is actually raining will depend
on the prior probability q that it typically rains in Seattle, and can
be found analytically through Bayes' Rule.

This module numerically approximates this probability in a manner that
converges for large numbers of tests.
"""
import argparse
import random

import numpy as np


def say(x, prob_lie):
    """
    x:        1 if actually raining, 0 if actually not raining
    prob_lie: probability that the friend will lie

    Returns 1 if the friend says it is raining, 0 otherwise
    """
    assert(0 <= prob_lie <= 1)
    assert(x == 1 or x == 0)
    if random.uniform(0, 1) > prob_lie:
        return x
    else:
        return x ^ 1


def test(num_iterations, prior, num_friends, prob_lie,
         give_denom=False):
    """
    Returns a dictionary where result['prob'] gives the experimentally
    determined probability of rain given that all friends said that it
    was raining.

    A "trial" first randomly picks whether or not rain occurred according to
    the prior probability. Then, it picks whether each of the friends
    are lying or not according to prob_lie. If all friends said that
    it was raining, then whether or not it actually rained is recorded in
    the statistics (for any other combination of friend responses, the trial
    is discarded).

    num_iterations: the number of trials
                    note that trials where all friends did not say yes count
                    toward num_iterations but are discarded from the
                    statistics
    prior:          the probability that it was raining before hearing
                    any responses from the friends
    num_friends:    the number of friends who independently say yes
    prob_lie:       the probability by which each friend independently lies
    give_denom:     if True, then add key 'denom' holding the number of
                    times all friends said yes out of all trials
    """
    assert(0 <= prior <= 1)
    assert(0 <= prob_lie <= 1)
    res = []

    for i in range(num_iterations):
        val = (random.uniform(0, 1) < prior)
        answers = [say(val, prob_lie) for k in range(num_friends)]
        if all(np.array(answers) == 1):
            res.append(val)

    # if res is empty, throw an error
    if len(res) == 0:
        err_msg = "The friends never all said yes"
        err_msg += ", try increasing num_iterations"
        raise RuntimeError(err_msg)

    percent_time_raining = {}
    percent_time_raining['prob'] = sum(res) / len(res)
    if give_denom:
        percent_time_raining['denom'] = len(res)
    return percent_time_raining


def analytic_answer(prior, num_friends, prob_lie):
    """
    Gives the probability of rain using Bayes' Rule
    """
    p_all_yes = (prior * (1 - prob_lie)**num_friends
                 + (1 - prior) * prob_lie**num_friends)
    if p_all_yes == 0:
        raise ValueError("With given params,"
                         "it is impossible for friends to say it is raining")
    p_all_yes_given_rain = (1 - prob_lie)**num_friends
    return p_all_yes_given_rain * prior / p_all_yes


if __name__ == "__main__":
    """
    Command line behavior
    """
    # sane defaults
    default_num_iterations = 1000000
    default_prior          = 0.3
    default_num_friends    = 3
    default_prob_lie       = 1. / 3.
    default_decimal_places = 3

    # argument parsing instructions
    desc = "Simulates the probability of rain in Seattle."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--iterations', dest='iter',
                        default=default_num_iterations,
                        help="number of trials to run")
    parser.add_argument('--prior', dest='prior',
                        default=default_prior,
                        help="prior probability of rain in Seattle")
    parser.add_argument('--nfriends', dest='nfriends',
                        default=default_num_friends,
                        help="number of friends in Seattle to call")
    parser.add_argument('--problie', dest='plie',
                        default=default_prob_lie,
                        help="probability that each friend lies")
    parser.add_argument('-v', '--verbose', dest='verb',
                        action='store_true',
                        help="output more information")
    parser.add_argument('-d', '--decimals', dest='dec',
                        default=default_decimal_places,
                        help="number of decimal places to output")
    parser.add_argument('-a', '--analytic', dest='analytic',
                        action='store_true',
                        help="calculate analytic solution with Bayes' Rule")
    args = parser.parse_args()

    num_iterations = int(args.iter)
    prior          = float(args.prior)
    nfriends       = int(args.nfriends)
    problie        = float(args.plie)
    ndec           = int(args.dec)

    # handle some invalid inputs
    if not ndec > 0:
        raise ValueError("Must show at least one decimal place")
    if not (0 <= prior <= 1):
        raise ValueError("Prior must be a probability from 0 to 1")
    if not (0 <= problie <= 1):
        raise ValueError("Probability of friend lying must be between 0 and 1")

    decimal_formatter = "{0:.%sf}" % str(ndec)

    if args.verb:
        print("You want to know if it is raining in Seattle")
        print("You call %s friends" % str(nfriends))
        print("  Each friend independently lies with probability %s"
              % decimal_formatter.format(problie))
        print("")
        print("It typically rains in Seattle with probability %s"
              % decimal_formatter.format(prior))
        if args.analytic:
            percent_time_raining = {'prob':
                                    analytic_answer(prior, nfriends, problie)}
        else:
            print("Simulating %s days" % str(num_iterations))
            percent_time_raining = test(num_iterations, prior, nfriends,
                                        problie, give_denom=True)
            print("  (on %s of these days all friends said yes)"
                  % str(percent_time_raining['denom']))
    else:
        if args.analytic:
            percent_time_raining = {'prob':
                                    analytic_answer(prior, nfriends, problie)}
        else:
            percent_time_raining = test(num_iterations, prior, nfriends,
                                        problie)

    print("Percent of time raining: %s"
          % decimal_formatter.format(percent_time_raining['prob']))
