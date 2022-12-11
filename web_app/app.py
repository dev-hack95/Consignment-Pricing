import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle




model = pickle.load(open("../notebooks/model.pkl", 'rb'))

#scalar = pickle.load(open('../notebooks/scaler.pkl', 'rb'))

st.write("""
# Consiment Price Prediction
""")

class get_dummies(BaseEstimator, TransformerMixin):
    def __init__(self, column_1=['PO / SO #', 'ASN/DN #', 'Fulfill Via', 'First Line Designation']):
        self.column_1 = column_1
    def fit(self):
        return self
    def transform(self):
            ohe = OneHotEncoder()
            return ohe.fit_transform(self.column_1)

class label_encoding(BaseEstimator, TransformerMixin):
    def __init__(self, column_2=['Managed By', 'Vendor INCO Term', 'Shipment Mode', 'Product Group', 'Sub Classification']):
        self.column_2 = column_2
    def fit(self, df):
        return self
    def transform(self, df):
        lb = LabelEncoder()
        return lb.fit_transform(self.column_2)

class feature_scaling(BaseEstimator, TransformerMixin):
    def __init__(self, column_3=['Weight (Kilograms)', 'Freight Cost (USD)']):
        self.column_3 = column_3
    def fit(self):
        return self
    def transform(self):
        min_max = MinMaxScaler()
        return min_max.fit_transform(self.column_3)    


pipe = Pipeline([
    ('dummies', get_dummies()),
    ('encode', label_encoding()),
    ('scaler', feature_scaling()),
])




po_so = st.selectbox('Select po_so', ['SCMS', 'SO'])
asn_dn = st.selectbox('Select asn_dsn', ['ASN', 'DN'])
managed_by = st.selectbox('Select managed_by', ['PMO - US', 'South Africa Field Office', 'Haiti Field Office', 'Ethiopia Field Office'])
fullfill_via = st.selectbox('Select fullfill_via', ['Direct Drop', 'From RDC'])
vendor_inco_term = st.selectbox('Select vendor_inco_term', ['EXW', 'FCA', 'DDU', 'CIP', 'DDP', 'CIF', 'N/A - From RDC', 'DAP'])
shipment_mode = st.selectbox('Select shipment_mode', ['Air', 'Other', 'Truck', 'Air Charter', 'Ocean'])
product_group = st.selectbox('Select product_group', ['HRDT', 'ARV', 'ACT', 'MRDT', 'ANTM'])
subclassification = st.selectbox('Select sub_classification', ['HIV test', 'Pediatric', 'Adult', 'HIV test - Ancillary', 'ACT', 'Malaria'])
designation = st.radio('Select designation', ['Yes', 'No'], index=0)
weight = st.number_input('Weight(kg)')
freight_cost = st.number_input('freight_cost')

data = [po_so, asn_dn, managed_by, fullfill_via, vendor_inco_term, shipment_mode, product_group, subclassification, designation, weight, freight_cost]
data = np.reshape(data, (1, -1))
new_data = pipe.fit_transform(data)
#print(new_data.shape)
prediction = model.predict(new_data)

submit = st.button('Predict')
if submit:
    st.write(prediction[0])