import numpy as np

from logistic_regression import logistic_regression_IRLS
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

from sklearn.linear_model import LogisticRegression as Regression


def read_dat(path):
	# raw text
	encode = "utf-8"
	with open(path, "r", encoding=encode) as f:
		while True:
			content = f.readline()
			if content[0] != "@":
				break
		content += f.read()
	# analysis
	data = [line.split(", ") for line in content.splitlines()]
	one_hot = {"Absent":0, "Present":1}
	for i,k in enumerate(data):
		data[i][4] = one_hot.get(k[4], -1)
	data = np.array(data, dtype=float)
	# input and output
	return data[:,:-1], data[:,-1].astype(int)

def evaluation(y_true, y_pred):
	# data
	c = confusion_matrix(y_true, y_pred)
	a = accuracy_score(y_true, y_pred)
	p = precision_score(y_true, y_pred)
	r = recall_score(y_true, y_pred)
	# output
	print("Accuracy classification score:  %.3f"%a)
	print("Precision classification score: %.3f"%p)
	print("Recal classification score:     %.3f"%r)
	print("Confusion matrix:\n%s"%c)


for i in range(5):
	train = "saheart-5-%dtra.dat"%(i+1)
	test  = "saheart-5-%dtst.dat"%(i+1)
	X_train,y_train = read_dat(train)
	X_test,y_test   = read_dat(test)

	model1 = logistic_regression_IRLS()
	model1.fit(X_train, y_train)

	model2 = Regression(solver="newton-cg")
	model2.fit(X_train, y_train)

	y_pred1 = model1.predict(X_test)
	y_pred2 = model2.predict(X_test)

	print(train, test)
	print("-"*37)
	print("IRIS Algorithm" + "-"*23)
	evaluation(y_test, y_pred1)
	print("LogisticRegression" + "-"*19)
	evaluation(y_test, y_pred2)
	print("-"*37, "\n"*3)
