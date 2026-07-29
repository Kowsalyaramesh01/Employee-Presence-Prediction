import pandas as pd
import joblib
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("dataset/employee_layoff_dataset.csv")

# ==============================
# DROP UNUSED
# ==============================
df = df.drop(['Employee_ID'], axis=1)

# ==============================
# SPLIT FEATURES
# ==============================
X = df.drop('Attrition', axis=1)
y = df['Attrition']

# ==============================
# IDENTIFY COLUMNS
# ==============================
cat_cols = X.select_dtypes(include='object').columns.tolist()
num_cols = X.select_dtypes(exclude='object').columns.tolist()

# ==============================
# ENCODING (SAFE FOR UNKNOWN)
# ==============================
encoder = OrdinalEncoder(
    handle_unknown='use_encoded_value',
    unknown_value=-1
)

X[cat_cols] = encoder.fit_transform(X[cat_cols])

# ==============================
# SCALING
# ==============================
scaler = StandardScaler()
X[num_cols] = scaler.fit_transform(X[num_cols])

# ==============================
# MODEL
# ==============================
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    class_weight='balanced',
    random_state=42
)

model.fit(X, y)

# ==============================
# SAVE EVERYTHING
# ==============================
joblib.dump(model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(cat_cols, "cat_cols.pkl")
joblib.dump(num_cols, "num_cols.pkl")

print("✅ Model trained successfully with safe encoding!")
