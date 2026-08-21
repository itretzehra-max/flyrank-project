import pandas as pd

# Load the dataset
df = pd.read_csv("sample_loan_data.csv")

print("=" * 50)
print("BIAS AUDIT REPORT")
print("=" * 50)

# 1. Check demographic representation (are groups balanced in the dataset itself?)
print("\n--- Demographic Representation ---")
group_counts = df["gender"].value_counts()
print(group_counts)

# 2. Check approval rate by group (the key bias signal)
print("\n--- Approval Rate by Group ---")
approval_rates = df.groupby("gender")["loan_approved"].mean().round(3) * 100
print(approval_rates)

# 3. Calculate the disparity between the highest and lowest approval rate
disparity = approval_rates.max() - approval_rates.min()
print(f"\nApproval rate disparity between groups: {disparity:.1f} percentage points")

# 4. Flag risk based on a common fairness threshold (80% rule / four-fifths rule)
ratio = approval_rates.min() / approval_rates.max()
print(f"Selection rate ratio (four-fifths rule check): {ratio:.2f}")

if ratio < 0.8:
    print("FLAG: Selection rate ratio is below 0.80 — this fails the four-fifths rule, "
          "a common regulatory red flag for adverse impact.")
else:
    print("PASS: Selection rate ratio meets the four-fifths rule threshold.")

# 5. Check if credit score (a legitimate factor) explains the gap, or if it's unexplained
print("\n--- Average Credit Score by Group (checking for a legitimate explanation) ---")
avg_credit = df.groupby("gender")["credit_score"].mean().round(1)
print(avg_credit)

credit_gap = avg_credit.max() - avg_credit.min()
print(f"\nCredit score gap between groups: {credit_gap:.1f} points")
print("\n--- Interpretation ---")
if disparity > 15 and credit_gap < 20:
    print("The approval gap is large relative to the small difference in credit scores, "
          "suggesting the gap may not be fully explained by credit risk alone. "
          "This warrants further investigation before deployment.")
