import math  
from phe import paillier
public_key, private_key = paillier.generate_paillier_keypair()
def linear_regression(y,x,xx,yy,xy):
    lr = {"slope":0,"intercept":0,"r2":0}
    n = len(y)
    sum_x = 0
    sum_y = 0
    sum_xy = 0
    sum_xx = 0
    sum_yy = 0



    for i in range(n):
        sum_x += x[i]
        sum_y += y[i]
        sum_xx += xx[i]
        sum_yy += yy[i]
        sum_xy += xy[i]
    

    lr["slope"] = (n * sum_xy - sum_x * sum_y) / (n*sum_xx - sum_x * sum_x)

    lr['intercept'] = (sum_y - lr["slope"] * sum_x)/n

    lr['r2'] = (n*sum_xy - sum_x*sum_y)/math.sqrt((n*sum_xx-sum_x*sum_x)*(n*sum_yy-sum_y*sum_y))**2

    return lr;


known_y = [1, 2, 3, 4]
known_x = [1, 2, 3, 4]
xx = [1,4,9,16]
yy = [1,4,9,16]
xy = [1,4,9,16]

lr = linear_regression(known_y, known_x,xx,yy,xy)


unknown_x = public_key.encrypt(-5)
#y = mx+ c
# pred = lr["slope"] * unknown_x + lr["intercept"]
print(private_key.raw_decrypt(unknown_x.ciphertext()))
print(private_key.decrypt(unknown_x))
