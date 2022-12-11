import os
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class get_dummies(BaseEstimator, TransformerMixin):
        def __init__(self, column_1=['PO / SO #', 'ASN/DN #', 'Fulfill Via', 'First Line Designation']):
            self.column_1 = column_1
        def fit(self, df):
            return self
        def transform(self, df):
            if (set(self.column_1).issubset(df.columns)):
                df[self.column_1] = pd.get_dummies(df[self.column_1], drop_first=True)
                return df
            else:
                print('Error')
                return df


class label_encoding(BaseEstimator, TransformerMixin):
        def __init__(self, column_2=['Managed By', 'Vendor INCO Term', 'Shipment Mode', 'Product Group', 'Sub Classification']):
            self.column_2 = column_2
        def fit(self, df):
            return self
        def transform(self, df):
            if (set(self.column_2).issubset(df.columns)):
                lb = LabelEncoder()
                for column in self.column_2:
                    df[column] = lb.fit_transform(df[column])
                return df
            else:
                print('Error')
                return df

class feature_scaling(BaseEstimator, TransformerMixin):
        def __init__(self, column_3=['Weight (Kilograms)', 'Freight Cost (USD)']):
            self.column_3 = column_3
        def fit(self, df):
            return self
        def transform(self, df):
            if (set(self.column_3).issubset(df.columns)):
                min_max = MinMaxScaler()
                df[self.column_3] = min_max.fit_transform(df[self.column_3])
                return df
            else:
                print("Error")
                return df

def replace_strings(df, feature):
        match feature:
            case 'Freight Cost (USD)':
                df[feature]=df[feature].replace("Freight Included in Commodity Cost",0)
                df.loc[df[feature].str.contains('See', na=False), feature] = 'test'
                df[feature] = df[feature].replace('test', 0)
                return df
            case 'Weight (Kilograms)':
                df[feature] = df[feature].replace('Weight Captured Separately', 0)
                df.loc[df[feature].str.contains('See', na=False), feature] = 'test'
                df[feature] = df[feature].replace('test', 0)
                return df
            case 'PO / SO #':
                df.loc[df[feature].str.contains('SCMS', na=False), feature] = 'SCMS'
                df.loc[df[feature].str.contains('SO', na=False), feature] = 'SO'
                return df
            case 'ASN/DN #':
                df.loc[df[feature].str.contains('ASN', na=False), feature] = 'ASN'
                df.loc[df[feature].str.contains('DN', na=False), feature] = 'DN'
                return df
            case _:
                print('Error')

def null_values(df, feature):
        match feature:
            case 'Line Item Insurance (USD)':
                df[feature] = df[feature].fillna(df['Line Item Insurance (USD)'].median())
                return df
            case 'Shipment Mode':
                df[feature]=df[feature].fillna("Other")
                return df
            case _:
                print('Error')

def outlier_thresholds_iqr(df, feature, th1, th3):
        Q1 = df[feature].quantile(th1)
        Q3 = df[feature].quantile(th3)
        IQR = Q3 - Q1
        upper_limit = Q3 + 3 * IQR
        lower_limit = Q1 - 1 * IQR
        return upper_limit, lower_limit

columns_list = ['Unit of Measure (Per Pack)',  'Line Item Value', 'Unit Price', 'Pack Price', 'Weight (Kilograms)', 'Freight Cost (USD)']

def check_outliers_iqr(df, feature):
    upper_limit, lower_limit = outlier_thresholds_iqr(df, feature, th1=0.25, th3=0.75)
    if df[(df[feature] > upper_limit) | (df[feature] < lower_limit)].any(axis=None):
        return True
    else:
        return False


def replace_with_thresholds_iqr(df, features, th1=0.25, th3=0.75, replace=True):
        data = []
        for feature in features:
            if feature != 'Outcome':
                outliers = check_outliers_iqr(df, feature)
                count = None
                upper_limit, lower_limit = outlier_thresholds_iqr(df, feature, th1=0.25, th3=0.75)
                if outliers:
                    count = df[(df[feature] > upper_limit) | (df[feature] < lower_limit)][feature].count()
                if replace:
                    if lower_limit < 0:
                        df.loc[(df[feature] > upper_limit), feature] = upper_limit
                    else:
                        df.loc[(df[feature] < lower_limit), feature] = lower_limit
                        df.loc[(df[feature] > upper_limit), feature] = upper_limit
            outliers_status = check_outliers_iqr(df, feature)
            data.append([outliers, outliers_status, count, feature, upper_limit, lower_limit ])

def drop_features(df, columns=['ID', 'Project Code',  'PQ First Sent to Client Date', 'PO Sent to Vendor Date', 'Scheduled Delivery Date', 'Delivered to Client Date', 'Delivery Recorded Date', 'Vendor', 'Item Description', 'Molecule/Test Type', 'Brand', 'Dosage', 'Dosage Form',  'Manufacturing Site', 'PQ #', 'Unit of Measure (Per Pack)', 'Line Item Quantity', 'Line Item Value', 'Pack Price', 'Unit Price']):
        if (set(columns).issubset(df.columns)):
            df.drop(columns,axis=1,inplace=True)
            return df
        else:
            print("One or more features are not in the dataframe")
            return df

pipe = Pipeline([
    ('dummies', get_dummies()),
    ('encode', label_encoding()),
    ('scaler', feature_scaling())])

def preprocess_data(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

    null_values(df, 'Line Item Insurance (USD)')
    null_values(df, 'Shipment Mode')

    replace_strings(df, 'Freight Cost (USD)')
    replace_strings(df, 'Weight (Kilograms)')
    replace_strings(df, 'PO / SO #')
    replace_strings(df, 'ASN/DN #')

    df = df[df["PO / SO #"] != 'DSCM-10090']
    df=df[(df["Freight Cost (USD)"]!='Invoiced Separately')]
    df['Freight Cost (USD)'] = df['Freight Cost (USD)'].astype('float')
    df['Weight (Kilograms)'] = df['Weight (Kilograms)'].astype('float')
    
    replace_with_thresholds_iqr(df, columns_list, th1=0.25, th3=0.75)
    
    drop_features(df)
    df.drop(['Country'], axis=1, inplace=True)

    pipe.fit_transform(df)


    df.to_csv(DATA_PATH[:-4] + "_processed.csv", index=False)


if __name__ == "__main__":
    DATA_PATH = os.path.abspath(sys.argv[1])
    preprocess_data(DATA_PATH)
    print("Saved to {}".format(DATA_PATH[:-4] + "_processed.csv"))
