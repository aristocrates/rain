"""
Get the probability that it is actually raining in Seattle.

Given that n friends in Seattle each lie with probability p, and each say
that it is raining, the probability that it is actually raining will depend
on the prior probability q that it typically rains in Seattle.
"""
import argparse
import random
import numpy as np

def say(x, prob_lie):
    """
    x:          1 if actually raining, 0 if actually not raining
    friend_lie: probability that the friend will lie

    Returns 1 if the friend says it is raining, 0 otherwise
    """
    assert(0 <= prob_lie <= 1)
    assert(x == 1 or x == 0)
    if random.uniform(0, 1) > prob_lie:
        return x
    else:
        return x ^ 1

def test(num_iterations, prior, num_friends, prob_lie,
         give_denom = False):
    """
    num_iterations: the number of times to run
    prior:          the probability that it is raining given no information
    num_friends:    the number of friends who independently say yes
    prob_lie:       the probability by which each friend independently lies
    give_denom:     if True, then output a tuple (
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

if __name__ == "__main__":
    default_num_iterations = 1000000
    default_prior = 0.3
    default_num_friends = 3
    default_prob_lie = 1. / 3.

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
    args = parser.parse_args()

    num_iterations = int(args.iter)
    prior          = float(args.prior)
    nfriends       = int(args.nfriends)
    problie        = float(args.plie)

    if not (0 <= prior <= 1):
        raise ValueError("Prior must be a probability from 0 to 1")
    if not (0 <= problie <= 1):
        raise ValueError("Probability of friend lying must be between 0 and 1")

    if args.verb:
        print("You want to know if it is raining in Seattle")
        print("You call %s friends" % str(nfriends))
        print("  Each friend independently lies with probability %s"
              % str(problie))
        print("")
        print("It typically rains in Seattle with probability %s" % str(prior))
        print("Simulating %s days" % str(num_iterations))
        percent_time_raining = test(num_iterations, prior, nfriends, problie,
                                    give_denom = True)
        print("  (on %s of these days all friends said yes)"
              % str(percent_time_raining['denom']))
    else:
        percent_time_raining = test(num_iterations, prior, nfriends, problie)

    print("Percent of time raining: %s" % str(percent_time_raining['prob']))
