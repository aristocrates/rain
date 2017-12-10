import sys
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

if __name__ == "__main__":
    default_num_iterations = 1000000
    default_prior = 0.3

    num_iterations = default_num_iterations
    prior = default_prior
    if len(sys.argv) > 1:
        num_iterations = int(sys.argv[1])
    if len(sys.argv) > 2:
        prior = float(sys.argv[2])
    if not (0 <= prior <= 1):
        raise ValueError("Prior must be a probability from 0 to 1")
    percent_time_raining = test(num_iterations, prior)
    print("Percent of time raining: %s" % str(percent_time_raining))
