import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.interactive(False)
plt.rcParams['figure.figsize'] = 15, 5

headers = ['SP', 'HIP', 'HCP', 'OPT', 'NS', 'NT', 'WHM',
           'PI', 'TM', 'VtoI', 'ItoC', 'AH', 'QInv']

# here we add a _-suffixed header after each header
# [sp, hip, ...] becomes [sp, sp_sent, hip, hip_sent, ...]
headers = ['language'] + [h.lower()
 for header in headers
 for h in (header, header + '_sent')]
headers[:5]
data = pd.read_csv('simulation-output3.csv', index_col=False, error_bad_lines=False)
data.columns = headers[:]
param_names = [p for p in data.columns
               if len(p) <= 4 and p != 'idk']

# the columns for the number of sentences consumed by the learner
sent_names = [p for p in data.columns
               if '_' in p]
for param in data.columns:
    data[param] = pd.to_numeric(data[param], errors='coerce')
len(data) - len(data.dropna(how='any', axis='index'))
data['language'] = data.language.astype(int).astype(str)
valid_rows = (
    data[param_names]
    .gt(1).replace(True, np.nan)
    .dropna()
).index
len(data) - len(valid_rows)
data = data.loc[valid_rows]
plt.boxplot(data)