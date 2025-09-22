import pandas as pd
import joblib

# --------------------------
# 1. Load new dataset (only features)
# --------------------------
new_df = pd.read_csv('newdataset.csv')  # CSV with StudentID, attendance, marks, attempts, fees_due

features = ['attendance', 'marks', 'attempts', 'fees_due']
X_new = new_df[features]

# --------------------------
# 2. Load trained model and encoders
# --------------------------
model = joblib.load('student_risk_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')

targets = ['attendance_risk', 'marks_risk', 'attempts_risk', 'fees_risk', 'dropout_risk']

# --------------------------
# 3. Predict risk labels
# --------------------------
y_new_pred_encoded = model.predict(X_new)

# Decode predictions back to G/O/R
y_new_pred = pd.DataFrame(y_new_pred_encoded, columns=targets)
for col in targets:
    le = label_encoders[col]
    y_new_pred[col] = le.inverse_transform(y_new_pred[col])

# --------------------------
# 4. Combine predictions with entire original dataset
# --------------------------
results_new = new_df.copy()  # Keep all original columns
results_new[targets] = y_new_pred  # Add predicted risk labels

# --------------------------
# 5. Save full dataset with predictions
# --------------------------
results_new.to_csv('new_students_with_predictions.csv', index=False)

print("Predictions saved to 'new_students_with_predictions.csv'")
print(results_new.head())
