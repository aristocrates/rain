rain
====

A project to simulate the probability that it is raining in Seattle.

Motivation
----------

If you ask your friends whether or not it is raining in Seattle right now,
and you can assume that each independently lies with some probability,
the probability that it is actually raining depends on the prior probability
of rain in Seattle, as this simulation shows.

Basic Assumptions
-----------------
 * **Consistency:** the friends all share the same truth, i.e. it is not
 possible for one friend to say that it is raining and be telling the truth,
 and for another friend to say that it is not raining and also be telling the
 truth (in a more realistic situation, it is possible that not all parts of
 Seattle receive rain, which could violate this assumption)
 * **Definitive prior:** you know before calling any of your friends that there
 is some probability that it is raining (i.e. based on weather forcasts)
 and you know the true value of this probability
 * **Independence of answers:** each friend will lie or tell the truth
 independent of the actions of all other friends (i.e. no collusion to lie
 or tell the truth to you)

Bayes' Rule
-----------

The probability that one friend says that it is raining can be obtained with
minimal computation if the probability that it is raining is known, and
therefore the probability that all friends say that it is raining.

In order to get the probability that it is raining given that all friends
said that it was, Bayes' Rule can be used:

  P(rain | all yes) = P(all yes | rain) * P(rain) / P(all yes)

The value P(all yes | rain) does not depend on the prior probability of rain,
but P(rain) is itself the prior probability of rain and P(all yes) depends
on this prior.

If the number of friends is n, and each friend lies with probability
P(lie) and tells the truth with probability (1 - P(lie))

  P(all yes) = P(rain) * ( (1 - P(lie)) )^n + (1 - P(rain)) * ( P(lie) )^n

  P(all yes | rain) = (1 - P(lie))^n

Some interesting observation(s):
 * If the probability of friends lying is 0.5, then mathematically the
 probability of rain will always be the same as the prior regardless of the
 number of friends. This makes sense because the response of a friend conveys
 no information if the response is equally likely to be true or false.
 * If the probability of friends lying is above 0.5, the posterior probability
 of rain decreases (often dramatically depending on the number of friends and
 how high the probability of lying is) given that all friends said yes.

Simulation
----------

In addition to an analytic solution (which can be run with
"python seattlerain.py [options] -a"), the module contains code to simulate
the problem. It does so by picking whether or not rain occurred according
to the prior, then picking whether each friend lies or does not lie. Out of
the times when all friends say it is raining, the fraction of times when it
is actually raining gives an approximation the posterior probability of rain.

Known difficult case(s):
 * When num_friends is large: because the probability that all friends will
 say that it is raining decays exponentially in the number of friends (when
 the probability of lying is non-zero), it is possible that there will not
 be a single iteration where all friends said yes. Possible solutions include
 increasing the number of iterations, decreasing the number of friends, or
 using the analytic solution.
 * When prob_lie and prior are both zero: it is impossible for any (let
 alone all) friends to say that it is raining. Thus the simulation fails in
 this case. The analytic solution is not defined in this case either.
