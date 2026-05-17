import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# load dataset
ads = pd.read_csv("Social_Network_Ads.csv")

# convert gender
ads['Gender'] = ads['Gender'].map({'Male':1,'Female':0})

# input and output
X = ads[['Gender','Age','EstimatedSalary']]
y = ads['Purchased']

# split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=2
)

# scaler
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# model
model = RandomForestClassifier()

# train
model.fit(X_train, y_train)

# accuracy
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print("Accuracy:", acc)

# save model
pickle.dump(model, open('model.pkl', 'wb'))

# save scaler
pickle.dump(scaler, open('scaler.pkl', 'wb'))

# save accuracy
with open('accuracy.txt', 'w') as f:
    f.write(str(round(acc * 100, 2)))

print("Model Saved Successfully")