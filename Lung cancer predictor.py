import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix


data = pd.read_csv("/home/ashraf/Documents/CSV files/cancer patient data sets.csv")
df = pd.DataFrame(data)
df['Level'] = df['Level'].map({'Low': 0, 'Medium': 1 , 'High': 2 })

X = df[["Coughing of Blood","Chest Pain","Weight Loss","Shortness of Breath","Smoking","Genetic Risk","Wheezing","Fatigue","Air Pollution","Passive Smoker"]]
y = df["Level"]


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100,random_state=42)
model.fit(X_train,y_train)
y_pred = model.predict(X_test)

print(accuracy_score(y_test,y_pred))


new_patient = np.array([[3,4,5,3,4,5,4,5,4,5]])

new_patient_scaled = scaler.transform(new_patient)

prediction = model.predict(new_patient_scaled)
risk_mapping = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
print("Prediction:", risk_mapping[prediction[0]])

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
