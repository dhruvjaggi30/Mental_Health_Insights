import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("Dataset with Anxiety and depression.csv")

df = df[['Anxiety Disorders - % of Population',
         'Depressive Disorders - % of Population']]

# Clean percentage values
for col in df.columns:
    df[col] = df[col].astype(str).str.replace('%', '')
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(inplace=True)

# Create target
def risk_label(row):
    avg = row.mean()
    if avg < 5:
        return "Low"
    elif avg < 10:
        return "Medium"
    else:
        return "High"

df['Risk'] = df.apply(risk_label, axis=1)

X = df.drop('Risk', axis=1)
y = df['Risk']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "mental_health_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model trained successfully")
