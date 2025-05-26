import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure output directory exists
os.makedirs("graphs", exist_ok=True)

# Load and prepare data
df = pd.read_csv("D:\\ai voice assistant\\logs\\generated_performance_logs_with_timestamp.csv")
df.columns = ["Timestamp", "Feature", "ExecutionTime(s)", "Status"]
df["SuccessBool"] = df["Status"].apply(lambda x: x.lower() == "success")

sns.set(style="whitegrid")
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titlesize"] = 14

# --- 1. Feature Usage Count ---
plt.figure(figsize=(12, 6))
usage_counts = df["Feature"].value_counts()
sns.barplot(x=usage_counts.index, y=usage_counts.values, palette="Blues_d")
plt.title("Feature Usage Count")
plt.xlabel("Feature")
plt.ylabel("Usage Count")
plt.xticks(rotation=45, ha='right')
for i, val in enumerate(usage_counts.values):
    plt.text(i, val + 0.5, str(val), ha='center')
plt.tight_layout()
plt.savefig("graphs/feature_usage.png")
plt.show()

# --- 2. Feature Success Rate ---
plt.figure(figsize=(12, 6))
success_rate = df.groupby("Feature")["SuccessBool"].mean() * 100
sns.barplot(x=success_rate.index, y=success_rate.values, palette="Greens")
plt.title("Feature Success Rate (%)")
plt.xlabel("Feature")
plt.ylabel("Success Rate (%)")
plt.ylim(0, 105)
plt.xticks(rotation=45, ha='right')
for i, val in enumerate(success_rate.values):
    plt.text(i, val + 2, f"{val:.1f}%", ha='center')
plt.tight_layout()
plt.savefig("graphs/feature_success_rate.png")
plt.show()

# --- 3. Average Execution Time ---
plt.figure(figsize=(12, 6))
avg_time = df.groupby("Feature")["ExecutionTime(s)"].mean()
sns.barplot(x=avg_time.index, y=avg_time.values, palette="Oranges")
plt.title("Average Execution Time per Feature (sec)")
plt.xlabel("Feature")
plt.ylabel("Avg Duration (s)")
plt.xticks(rotation=45, ha='right')
for i, val in enumerate(avg_time.values):
    plt.text(i, val + 0.01, f"{val:.2f}", ha='center')
plt.tight_layout()
plt.savefig("graphs/avg_execution_time.png")
plt.show()


df["Timestamp"] = pd.to_datetime(df["Timestamp"])
usage_time = df.groupby([df["Timestamp"].dt.date, "Feature"]).size().unstack(fill_value=0)

plt.figure(figsize=(12, 6))
for feature in usage_time.columns:
    plt.plot(usage_time.index, usage_time[feature], linestyle=':', marker='o', label=feature)
plt.title("Feature Usage Over Time (Dotted Plot)")
plt.xlabel("Date")
plt.ylabel("Usage Count")
plt.xticks(rotation=45)
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig("graphs/dotted_feature_usage_over_time.png")
plt.show()


success_time = df.groupby([df["Timestamp"].dt.date, "Feature"])["SuccessBool"].mean().unstack(fill_value=0) * 100

plt.figure(figsize=(12, 6))
for feature in success_time.columns:
    plt.plot(success_time.index, success_time[feature], linestyle=':', marker='o', label=feature)
plt.title("Success Rate Over Time (Dotted Plot)")
plt.xlabel("Date")
plt.ylabel("Success Rate (%)")
plt.ylim(0, 105)
plt.xticks(rotation=45)
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig("graphs/dotted_success_rate_over_time.png")
plt.show()


avg_time_series = df.groupby([df["Timestamp"].dt.date, "Feature"])["ExecutionTime(s)"].mean().unstack(fill_value=0)

plt.figure(figsize=(12, 6))
for feature in avg_time_series.columns:
    plt.plot(avg_time_series.index, avg_time_series[feature], linestyle=':', marker='o', label=feature)
plt.title("Average Execution Time Over Time (Dotted Plot)")
plt.xlabel("Date")
plt.ylabel("Avg Time (s)")
plt.xticks(rotation=45)
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig("graphs/dotted_avg_exec_time_over_time.png")
plt.show()


from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

# Dummy predicted status (assume all should succeed), compare with actual
y_true = df["Status"].apply(lambda x: "Success" if x.lower() == "success" else "Fail")
y_pred = ["Success"] * len(y_true)  # You can replace this with real predictions if any

cm = confusion_matrix(y_true, y_pred, labels=["Success", "Fail"], normalize="true")
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Success", "Fail"])

plt.figure(figsize=(6, 6))
disp.plot(cmap=plt.cm.Blues, values_format=".2f")
plt.title("Normalized Confusion Matrix (Success vs. Predicted Success)")
plt.savefig("graphs/normalized_confusion_matrix.png")
plt.show()
