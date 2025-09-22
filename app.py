import pandas as pd

# Load your CSV
df = pd.read_csv("updated_file.csv")

# Function to classify attendance
def attendance_risk(att):
    if att < 65:
        return 'R'
    elif 65 <= att <= 75:
        return 'O'
    else:
        return 'G'

# Function to classify marks
def marks_risk(mark):
    if mark < 24:
        return 'R'
    elif 24 <= mark <= 60:
        return 'O'
    else:
        return 'G'

# Function to classify attempts
def attempts_risk(attempt):
    if attempt > 15:
        return 'R'
    elif 7 <= attempt <= 15:
        return 'O'
    else:
        return 'G'

# Function to classify fees_due (assuming value in INR)
def fees_risk(fee):
    if fee > 80000:
        return 'R'
    elif 50000 <= fee <= 80000:
        return 'O'
    else:
        return 'G'

# Apply functions to create risk columns
df['attendance_risk'] = df['attendance'].apply(attendance_risk)
df['marks_risk'] = df['marks'].apply(marks_risk)
df['attempts_risk'] = df['attempts'].apply(attempts_risk)
df['fees_risk'] = df['fees_due'].apply(fees_risk)

# Function to calculate dropout_risk
def dropout_risk(row):
    # High risk conditions
    if row['attendance_risk'] == 'R' or row['fees_risk'] == 'R':
        return 'R'
    if row['marks_risk'] == 'R' and row['attempts_risk'] == 'R':
        return 'R'
    # Moderate risk conditions
    if row['attendance_risk'] == 'O' or row['fees_risk'] == 'O':
        return 'O'
    if row['marks_risk'] == 'O' and row['attempts_risk'] == 'O':
        return 'O'
    # If none of the above, low risk
    return 'G'

# Apply the dropout risk function
df['dropout_risk'] = df.apply(dropout_risk, axis=1)

# Save updated CSV
df.to_csv("students_with_risk.csv", index=False)

print("Dropout risk prediction completed! ✅")
