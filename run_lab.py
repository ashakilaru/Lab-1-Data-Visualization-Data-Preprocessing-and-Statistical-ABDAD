import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

print('Starting lab runner...')
root = os.path.dirname(__file__)
os.makedirs(os.path.join(root, 'data'), exist_ok=True)
os.makedirs(os.path.join(root, 'screenshots'), exist_ok=True)

# Load dataset
data_path = os.path.join(root, 'data', 'tips.csv')
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    print('Loaded existing data/tips.csv')
else:
    try:
        df = sns.load_dataset('tips')
        df.to_csv(data_path, index=False)
        print('Downloaded tips dataset and saved to data/tips.csv')
    except Exception as e:
        raise RuntimeError('Failed to load tips dataset: ' + str(e))

# Save head snapshot
df.head().to_csv(os.path.join(root, 'screenshots', 'df_head_before.csv'), index=False)

# Visualizations
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='total_bill', y='tip', hue='time')
plt.title('Total Bill vs Tip by Time of Day')
plt.tight_layout()
plt.savefig(os.path.join(root, 'screenshots', 'scatter_totalbill_tip.png'))
plt.close()

plt.figure(figsize=(8,5))
sns.histplot(df['total_bill'], bins=20, kde=True)
plt.title('Distribution of Total Bill')
plt.tight_layout()
plt.savefig(os.path.join(root, 'screenshots', 'hist_total_bill.png'))
plt.close()

plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='day', y='tip')
plt.title('Tip Distribution by Day')
plt.tight_layout()
plt.savefig(os.path.join(root, 'screenshots', 'boxplot_tip_by_day.png'))
plt.close()

print('Saved visualizations.')

# 3.1 Missing values (introduce small NaNs and impute)
missing_before = df.isnull().sum()
missing_before.to_csv(os.path.join(root, 'screenshots', 'missing_before.csv'))

df_mv = df.copy()
np.random.seed(0)
mask = np.random.rand(len(df_mv)) < 0.02
df_mv.loc[mask, 'total_bill'] = np.nan
mask2 = np.random.rand(len(df_mv)) < 0.02
df_mv.loc[mask2, 'tip'] = np.nan

df_mv.head(10).to_csv(os.path.join(root, 'screenshots', 'df_with_missing_before.csv'), index=False)

# Impute
if df_mv['total_bill'].isnull().any():
    df_mv['total_bill'].fillna(df_mv['total_bill'].mean(), inplace=True)
if df_mv['tip'].isnull().any():
    df_mv['tip'].fillna(df_mv['tip'].mean(), inplace=True)

df_mv.head(10).to_csv(os.path.join(root, 'screenshots', 'df_with_missing_after.csv'), index=False)
print('Handled missing values (mean imputation).')

# 3.2 Outlier detection IQR for total_bill
Q1 = df['total_bill'].quantile(0.25)
Q3 = df['total_bill'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df['total_bill'] < lower) | (df['total_bill'] > upper)]

with open(os.path.join(root, 'screenshots', 'iqr_info.txt'), 'w') as f:
    f.write(f'Q1={Q1}\nQ3={Q3}\nIQR={IQR}\nlower={lower}\nupper={upper}\n')
outliers.to_csv(os.path.join(root, 'screenshots', 'outliers_total_bill.csv'), index=False)

df_no_out = df[(df['total_bill'] >= lower) & (df['total_bill'] <= upper)].copy()
df_no_out.to_csv(os.path.join(root, 'screenshots', 'df_after_outlier_removal.csv'), index=False)
print('Outlier detection and removal completed.')

# 3.3 Data reduction: sampling and drop
df.copy().to_csv(os.path.join(root, 'screenshots', 'df_before_reduction.csv'), index=False)
df_sampled = df.sample(frac=0.5, random_state=1).reset_index(drop=True)
if 'sex' in df_sampled.columns:
    df_sampled_drop = df_sampled.drop(columns=['sex'])
else:
    df_sampled_drop = df_sampled

df_sampled_drop.to_csv(os.path.join(root, 'screenshots', 'df_after_reduction.csv'), index=False)
print('Data reduction snapshots saved.')

# 3.4 Scaling and discretization
scale_df = df[['total_bill', 'tip']].copy()
scale_df.head().to_csv(os.path.join(root, 'screenshots', 'df_before_scaling.csv'), index=False)
scaler = MinMaxScaler()
scale_df[['total_bill_scaled','tip_scaled']] = scaler.fit_transform(scale_df[['total_bill','tip']])
scale_df.head().to_csv(os.path.join(root, 'screenshots', 'df_after_scaling.csv'), index=False)

# Discretize
try:
    df['total_bill_cat'] = pd.cut(df['total_bill'], bins=3, labels=['Low','Medium','High'])
    df[['total_bill','total_bill_cat']].head().to_csv(os.path.join(root, 'screenshots', 'df_after_discretization.csv'), index=False)
except Exception:
    pass
print('Scaling and discretization done.')

# Step 4: Statistical analysis
with open(os.path.join(root, 'screenshots', 'data_info.txt'), 'w') as f:
    df.info(buf=f)

desc = df.describe(include='all')
desc.to_csv(os.path.join(root, 'screenshots', 'describe_all.csv'))
print('Saved .info() and .describe() outputs.')

# Central tendency
central = {}
for col in df.select_dtypes(include=[np.number]).columns:
    central[col] = {
        'min': float(df[col].min()),
        'max': float(df[col].max()),
        'mean': float(df[col].mean()),
        'median': float(df[col].median()),
        'mode': list(df[col].mode().values)
    }
pd.DataFrame(central).to_csv(os.path.join(root, 'screenshots', 'central_tendency.csv'))
print('Saved central tendency measures.')

# Dispersion
disp = {}
for col in df.select_dtypes(include=[np.number]).columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    disp[col] = {
        'range': float(df[col].max() - df[col].min()),
        'q1': float(q1),
        'q3': float(q3),
        'iqr': float(iqr),
        'variance': float(df[col].var()),
        'std_dev': float(df[col].std())
    }
pd.DataFrame(disp).to_csv(os.path.join(root, 'screenshots', 'dispersion_measures.csv'))
print('Saved dispersion measures.')

# Correlation
corr = df.select_dtypes(include=[np.number]).corr()
corr.to_csv(os.path.join(root, 'screenshots', 'correlation_matrix.csv'))
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Matrix (numeric columns)')
plt.tight_layout()
plt.savefig(os.path.join(root, 'screenshots', 'correlation_heatmap.png'))
plt.close()
print('Saved correlation heatmap and matrix.')

print('Lab runner finished. Check the screenshots/ directory for outputs.')
