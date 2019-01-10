from fractions import Fraction

n1=0x5ffa391905f026a9e64eec553e37209938977ac11d1ef969d3848a9e2f77dd33fc12fb698b872ba1bd3bf5ac6e02a1fd24e6c26f95790f7a21e3f51a806919cd7254a7bb1ec3a23d7c0f7e773ffce083f09daaf34ef84b25df14c8114ce4b4fbf7b20646ea23aef46b51e62f395c966f20c906a1dea3a909e9d4093503ebd833
e1=0x2025b7ef3c7484a7ed9da144c3b92159fad4a7bd4159fd16b83256d92814fb09ee8f13606ed4982afa69e518511e9b0f0fc3d9220dca82a416a4ec9891adf48b242a2e3e2dd5fc0f685aff1817c29a47ee83977a3253af1a0d6dcc3ae1806d0dc8f9c247e19bd5b8305ebad0c043b356c7d81d9e9f927e2f833ccf862b521063

def main():
    print(hex(n1))


def recursive_fraction(a):
    if len(a) == 1:
        return a[0]
    else:
        a0 = a[0]
        a.pop(0)
        b = recursive_fraction(a)
        return a0 + 1/Fraction(b)


def factorize(e, n):
    i = 0
    r = [0]
    qi = [0]
    solved = False

    while not solved:
        if i == 0:
            qi[0] = int(e/n) #int rounds down
            ai = Fraction(qi[i] + 1)
            r[0] = (Fraction(str(e) + '/' + str(n)) - int(qi[i]))
        else:
            qi.append(int(1/r[i-1])) #r = residue from last round
            qi_temp = qi.copy()
            if i % 2 == 0:
                qi_temp[i] += 1
                solved = True

            ai = Fraction(recursive_fraction(qi_temp))
            r.append(1/Fraction(str(r[i-1]))-qi[i])

        k = ai.numerator
        dg = ai.denominator

        print("a0= " + str(ai))
        print("k= " + str(k) + ", dg= " + str(dg))

        #if k==1 the candidates are wrong
        if k != 1:
            g = e * dg - k * int(e * dg / k)
            print("g = " + str(g))

        i += 1


if __name__ == "__main__":
    #e=2621
    #n=8927
    #print((Fraction(str(e) + '/' + str(n)) - 1))
    factorize(2621, 8927)
    #factorize(n1, e1)
