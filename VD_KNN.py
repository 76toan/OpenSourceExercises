import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy import array
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.metrics import mean_squared_error, \
                            mean_absolute_error

df=pd.read_csv('Student_Performance.csv')#,index_col=0,header = 0)
x = array(df.iloc[:200,0:5]).astype(np.float64)
y = array(df.iloc[:200,4:5]).astype(np.float64)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
knn = neighbors.KNeighborsRegressor(n_neighbors = 3,p=2)
knn.fit(X_train, y_train)
y_predict = knn.predict(X_test)
print('mse score: %.2f' % mean_squared_error(y_test,y_predict))
print('mae score: %.2f' % mean_absolute_error(y_test,y_predict))
print('RMSE:', np.sqrt(mean_squared_error(y_test, y_predict)))
plt.plot(range(0,len(y_test)), y_test, 'ro', label ='Original data')
plt.plot(range(0,len(y_predict)), y_predict,'bo', label ='Fitted line')
for i in range(0,len(y_test)):
    tam = [y_test[i],y_predict[i]]
    plt.plot([i,i],tam,'Green')
#plt.plot(range(0,len(y_predict)), abs(y_predict-y_test),'g', label ='Error distance')
plt.title('KNN Result')
plt.legend()
plt.show()
