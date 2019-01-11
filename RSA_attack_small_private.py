########################
# This module implements an algorithm to attack RSA with short private exponent d
# Rule of thumb: The attack works if the number of bits of d is shorter than 1/4 the number of bits of n=p*q
# todos:
# - performance optimizations
# - does not pause if no solution is found
##########################
from fractions import Fraction
from decimal import Decimal
import numpy as np
import math


# calculates continued fraction of a list 'a'
def recursive_fraction(l):
    a = l.copy()
    if len(a) == 1:
        return a[0]
    else:
        a0 = a[0]
        a.pop(0)
        b = recursive_fraction(a)
        return a0 + 1/Fraction(b)


# factorize n (this is the attack)
def factorize(e, n):
    i = 0
    r = [0]
    qi = [0]
    solved = False

    # continue until a solution was found
    while not solved:
        if i == 0:
            # round down e/n
            qi[0] = int(e/n)
            # calculate approximation ai
            ai = Fraction(qi[i] + 1)
            # calculate residue
            r[0] = (Fraction(str(e) + '/' + str(n)) - int(qi[i]))
        else:
            if i == 381:
                print("hello")
            # round down 1/residue_from_last_iteration
            qi.append(int(1/r[i-1]))
            # copy list for usage
            qi_temp = qi.copy()
            # if iteration_number is equal: the last qi value needs to be +1
            if i % 2 == 0:
                qi_temp[i] += 1

            # calculate approximation ai
            ai = Fraction(recursive_fraction(qi_temp))
            # calculate residue
            r.append(1/Fraction(str(r[i-1]))-qi[i])

        # calculate solution candidates
        k = ai.numerator
        dg = ai.denominator

        print("checking candidates (i = " + str(i) + "): k= " + str(k) + ", dg= " + str(dg))

        # if k==1 the candidates are wrong
        if k != 1:
            edg_k = int(e * dg / k)
            g = e * dg - k * edg_k
            #print("g = " + str(g))

            p_plus_q = - edg_k + n + 1
            #print("p + q = " + str(p_plus_q))

            # calculate roots of x^2-(p+q)x+n
            # x1,2 = p_plus_q/2 -/+ math.sqrt(pow(-p_plus_q/2, 2)-n)
            tmp = Fraction(p_plus_q / 2)
            tmp_s = np.power(tmp, 2)
            tmp_s = Fraction(tmp_s / 4)
            tmp_s_n = Fraction(tmp_s - n)
            x1_n = Decimal.sqrt(Decimal(tmp_s_n.numerator))
            x1_d = Decimal.sqrt(Decimal(tmp_s_n.denominator))
            x1 = tmp + Fraction(x1_n/x1_d)
            x2 = tmp - Fraction(x1_n/x1_d)
            #x2 = tmp - np.sqrt(tmp_s_n)

            # final check
            if(x1 * x2 == n):
                solved = True
                print("solution found: ")
                print("p = " + str(x1) + ", q = " + str(x2))
        i += 1


if __name__ == "__main__":
    #homework variables
    n1 = 0x5ffa391905f026a9e64eec553e37209938977ac11d1ef969d3848a9e2f77dd33fc12fb698b872ba1bd3bf5ac6e02a1fd24e6c26f95790f7a21e3f51a806919cd7254a7bb1ec3a23d7c0f7e773ffce083f09daaf34ef84b25df14c8114ce4b4fbf7b20646ea23aef46b51e62f395c966f20c906a1dea3a909e9d4093503ebd833
    e1 = 0x2025b7ef3c7484a7ed9da144c3b92159fad4a7bd4159fd16b83256d92814fb09ee8f13606ed4982afa69e518511e9b0f0fc3d9220dca82a416a4ec9891adf48b242a2e3e2dd5fc0f685aff1817c29a47ee83977a3253af1a0d6dcc3ae1806d0dc8f9c247e19bd5b8305ebad0c043b356c7d81d9e9f927e2f833ccf862b521063

    #factorize(2621, 8927)
    factorize(n1, e1)
