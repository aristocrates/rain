import argparse
import random
import numpy as np

# 1 means raining, 0 means not raining
def say(x):
    if random.uniform(0, 1) * 3 > 1:
        return x
    else:
        return x ^ 1

def test(num_iterations, prior):
    res = []

    for i in range(num_iterations):
        val = (random.uniform(0, 1) < prior)
        answers = [say(val) for k in range(3)]
        if all(np.array(answers) == 1):
            res.append(val)        
            
    percent_time_raining = sum(res) / len(res)
    return percent_time_raining

def usage():
    return """python seattlerain.py [iterations] [prior]"""

if __name__ == "__main__":
    default_num_iterations = 1000000
    default_prior = 0.3

    desc = "Simulates the probability of rain in Seattle."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--iterations', dest='iter',
                        default=default_num_iterations,
                        help="number of trials to run")

    parser.add_argument('--prior', dest='prior',
                        default=default_prior,
                        help="prior probability of rain in Seattle")
    args = parser.parse_args()

    num_iterations = int(args.iter)
    prior = float(args.prior)

    if not (0 <= prior <= 1):
        raise ValueError("Prior must be a probability from 0 to 1")

    percent_time_raining = test(num_iterations, prior)
    print("Percent of time raining: %s" % str(percent_time_raining))
