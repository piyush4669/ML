import math
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from numpy import loadtxt, where


from phe import paillier
public_key, private_key = paillier.generate_paillier_keypair()



# scale larger positive and values to between -1,1 depending on the largest
# value in the data
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
df = pd.read_csv("./data.csv", header=0)

# clean up data
df.columns = ["index","grade1","grade2","label"]

# formats the input data into two arrays, one of independant variables
# and one of the dependant variable
X = df[["grade1","grade2"]]
X = np.array(X)
X = min_max_scaler.fit_transform(X)
Y = df["label"]
Y = np.array(Y)

# print(X)
# print("__"*60)
# print(Y)

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.01)


##The sigmoid function adjusts the cost function hypotheses to adjust the algorithm proportionally for worse estimations
def Sigmoid(z):
	G_of_Z = float(1.0 / float((1.0 + math.exp(-1.0*z))))
	return G_of_Z 

##The hypothesis is the linear combination of all the known factors x[i] and their current estimated coefficients theta[i] 
##This hypothesis will be used to calculate each instance of the Cost Function
def Hypothesis(theta, x):
	z = 0
	for i in range(len(theta)):
		z += x[i]*theta[i]
	return Sigmoid(z)

##For each member of the dataset, the result (Y) determines which variation of the cost function is used
##The Y = 0 cost function punishes high probability estimations, and the Y = 1 it punishes low scores
##The "punishment" makes the change in the gradient of ThetaCurrent - Average(CostFunction(Dataset)) greater
def Cost_Function(X,Y,theta,m):
	sumOfErrors = 0
	for i in range(m):
		xi = X[i]
		hi = Hypothesis(theta,xi)
		if Y[i] == 1:
			error = Y[i] * math.log(hi)
		elif Y[i] == 0:
			error = (1-Y[i]) * math.log(1-hi)
		sumOfErrors += error
	const = -1/m
	J = const * sumOfErrors
	# print ('cost is ', J )
	return J

##This function creates the gradient component for each Theta value 
##The gradient is the partial derivative by Theta of the current value of theta minus 
##a "learning speed factor aplha" times the average of all the cost functions for that theta
##For each Theta there is a cost function calculated for each member of the dataset
def Cost_Function_Derivative(X,Y,theta,j,m,alpha):
	sumErrors = 0
	for i in range(m):
		xi = X[i]
		xij = xi[j]
		hi = Hypothesis(theta,X[i])
		error = (hi - Y[i])*xij
		sumErrors += error
	m = len(Y)
	constant = float(alpha)/float(m)
	J = constant * sumErrors
	return J

##For each theta, the partial differential 
##The gradient, or vector from the current point in Theta-space (each theta value is its own dimension) to the more accurate point, 
##is the vector with each dimensional component being the partial differential for each theta value
def Gradient_Descent(X,Y,theta,m,alpha):
	new_theta = []
	constant = alpha/m
	for j in range(len(theta)):
		CFDerivative = Cost_Function_Derivative(X,Y,theta,j,m,alpha)
		new_theta_value = theta[j] - CFDerivative
		new_theta.append(new_theta_value)
	return new_theta

##The high level function for the LR algorithm which, for a number of steps (num_iters) finds gradients which take 
##the Theta values (coefficients of known factors) from an estimation closer (new_theta) to their "optimum estimation" which is the
##set of values best representing the system in a linear combination model
def Logistic_Regression(X,Y,alpha,theta,num_iters):
	m = len(Y)
	for x in range(num_iters):
		new_theta = Gradient_Descent(X,Y,theta,m,alpha)
		theta = new_theta
		if x % 100 == 0:
			#here the cost function is used to present the final hypothesis of the model in the same form for each gradient-step iteration
			Cost_Function(X,Y,theta,m)
			# print ('theta ', theta)	
			# print ('cost is ', Cost_Function(X,Y,theta,m))
	return theta

# ##The sigmoid function adjusts the cost function hypotheses to adjust the algorithm proportionally for worse estimations
# def Sigmoid(z):
# 	G_of_Z = float(1.0 / float((1.0 + math.exp(-1.0*z))))
# 	return G_of_Z 

##The hypothesis is the linear combination of all the known factors x[i] and their current estimated coefficients theta[i] 
##This hypothesis will be used to calculate each instance of the Cost Function
def Hypothesis2(theta, x):
	z = 0
	for i in range(len(theta)):
		z += x[i]*theta[i]
	return z
   

initial_theta = [0,0]
alpha = 0.1
iterations = 1000
theta = Logistic_Regression(X_train,Y_train,alpha,initial_theta,iterations)
prediction = Hypothesis2(theta,[public_key.encrypt(0.27),public_key.encrypt(0.005)])
print(prediction)
print(1 if private_key.decrypt(prediction) > 0 else 0)
# score = 0
# length = len(X_test)
# for i in range(length):
#     prediction = round(Hypothesis(theta,X_test[i]))
#     answer = Y_test[i]
#     if prediction == answer:
#         score += 1
# print (str(score) +"/"+str(length))

# score = 0
# length = len(X_test)
# for i in range(length):
#     prediction = round(Hypothesis2(theta,X_test[i]))
#     answer = Y_test[i]
#     if prediction == answer:
#         score += 1
# print (str(score) +"/"+str(length))