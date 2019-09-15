import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler #normalizes/scales data inputs as their ranges can vary
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score


print ("hello beatriz")
dataset = pd.read_csv('diabetes.csv')
print ("Data Set Length: " + len(dataset))
print (dataset.head())

#replace zeroes
zero_not_accepted = ['Glucose','BloodPressure','SkinThickness', 'BMI', 'Insulin']
for column in zero_not_accepted:
	dataset[column] = dataset[column].replace(0,np.NAN)
	mean = int(dataset[column].mean(skipna=True))
	dataset[column] = dataset[column].replace(np.NAN, mean)
	
#split dataset to test training against subset dataset
X = dataset.iloc[:,0:8] #all rows, only want columns 0-7, column index 8 is outcome and not used to train, that's the answer
y = dataset.iloc[:,8] #all rows, only outcome column
X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=0, test_size=0.2)

#Feature scaling
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

#Define the model: Init K-NN
classifi