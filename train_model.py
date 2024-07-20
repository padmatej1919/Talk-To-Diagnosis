import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

data = pd.read_csv('D:\\Talk-To-Diagnosis\\DatasetForTreatment.csv')

X = data.drop(columns=['PatientID', 'RecommendedTreatmentPlan'])
y = data['RecommendedTreatmentPlan']


numeric_features = ['Age']
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())])

categorical_features = ['Gender', 'MedicalHistory', 'GeneticMarkers', 'LifestyleFactors', 'CurrentMedications']
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])


model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model.fit(X_train, y_train)


y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)
# print(classification_report(y_test, y_pred))
with open('report.txt', 'w') as f:
    f.write(report)

joblib.dump(model, 'treatment_model.joblib')


model = joblib.load('treatment_model.joblib')
new_data = pd.DataFrame({
    'Age': [21],
    'Gender': ['Male'],
    'MedicalHistory': ['Anemia'],
    'GeneticMarkers': ['HLA-B27: Positive'],
    'LifestyleFactors': ['Smoker: No, Alcohol: Moderate, Diet: Low Sodium'],
    'CurrentMedications': ['Iron Supplements']
})
new_pred = model.predict(new_data)
print(new_pred)
