import pandas as pd

def preprocess(df,region_df):
    df1 = df[df['Season'] == 'Summer']
    df2 = df1.merge(region_df, on='NOC', how='left')
    df3 = pd.concat([df2, pd.get_dummies(df2['Medal'])], axis=1)
    return df3