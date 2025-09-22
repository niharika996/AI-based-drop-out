# multioutput_student_risk_eval.py
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# --------------------------
# 1. Load dataset
# --------------------------
# Replace with your CSV file path
df = pd.read_csv('students_with_risk.csv')

# --------------------------
# 2. Define features and target columns
# --------------------------
features = ['attendance', 'marks', 'attempts', 'fees_due']
targets = ['attendance_risk', 'marks_risk', 'attempts_risk', 'fees_risk', 'dropout_risk']

X = df[features]
y = df[targets]

# --------------------------
# 3. Encode target labels (G=0, O=1, R=2)
# --------------------------
label_encoders = {}
y_encoded = pd.DataFrame()

for col in targets:
    le = LabelEncoder()
    y_encoded[col] = le.fit_transform(y[col])
    label_encoders[col] = le

# --------------------------
# 4. Train/test split
# --------------------------
# First 150 rows for training, last 50 for testing
X_train, X_test = X.iloc[:150], X.iloc[150:]
y_train, y_test = y_encoded.iloc[:150], y_encoded.iloc[150:]

# --------------------------
# 5. Train MultiOutput Random Forest
# --------------------------
model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
model.fit(X_train, y_train)

# --------------------------
# 6. Predict on test set
# --------------------------
y_pred_encoded = model.predict(X_test)

# --------------------------
# 7. Decode predictions back to G/O/R
# --------------------------
y_pred = pd.DataFrame(y_pred_encoded, columns=targets)

for col in targets:
    le = label_encoders[col]
    y_pred[col] = le.inverse_transform(y_pred[col])

# --------------------------
# 8. Decode y_test for comparison
# --------------------------
y_test_decoded = pd.DataFrame()
for col in targets:
    le = label_encoders[col]
    y_test_decoded[col] = le.inverse_transform(y_test[col])

# --------------------------
# 9. Combine predictions and actual values
# --------------------------
results = X_test.copy()
for col in targets:
    results[col + '_actual'] = y_test_decoded[col]
    results[col + '_pred'] = y_pred[col]

print("Predictions vs Actuals for test students:")
print(results)

# --------------------------
# 10. Evaluate performance
# --------------------------
print("\nClassification Report per risk label:\n")
for col in targets:
    print(f"--- {col} ---")
    print(classification_report(y_test_decoded[col], y_pred[col]))

# Optional: overall accuracy per label
print("\nAccuracy per risk label:")
for col in targets:
    acc = accuracy_score(y_test_decoded[col], y_pred[col])
    print(f"{col}: {acc:.2f}")

# --------------------------
# Overall accuracy: all 5 labels correct per student
# --------------------------

# Compare predicted vs actual for all 5 labels
all_correct = (y_pred == y_test_decoded).all(axis=1)

# Count how many students are completely correct
num_correct = all_correct.sum()
total_students = len(all_correct)

overall_accuracy = num_correct / total_students
print(f"\nOverall student-level accuracy (all 5 labels correct): {overall_accuracy:.2%}")



# Save the trained model
joblib.dump(model, 'student_risk_model.pkl')

# Save the label encoders
joblib.dump(label_encoders, 'label_encoders.pkl')

print("\nModel and label encoders saved!")
