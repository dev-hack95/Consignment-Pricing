import streamlit as st
import numpy as np
import pickle

model = pickle.load(open("./models/model.pkl", 'rb'))
scaler = pickle.load(open("./models/scaler.pkl", 'rb'))
st.write("""
# Consignment Price Prediction
""")


po_so = st.radio('Select po_so', ['SCMS', 'SO'])
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

if po_so == 'SCMS':
    po_so = 0
else:
    po_so = 1

if asn_dn == 'ASN':
    asn_dn = 0
else:
    asn_dn = 1

if managed_by == 'PMO - US':
    managed_by = 2
else:
    managed_by = 0

if fullfill_via == 'Direct Drop':
    fullfill_via = 0
else:
    fullfill_via = 1

if vendor_inco_term == 'N/A - From RDC':
    vendor_inco_term = 7
elif vendor_inco_term == 'EXW':
    vendor_inco_term = 5
elif vendor_inco_term == 'DDP':
    vendor_inco_term = 3
elif vendor_inco_term == 'FCA':
    vendor_inco_term = 6
elif vendor_inco_term == 'CIP':
    vendor_inco_term = 1
elif vendor_inco_term == 'DDU':
    vendor_inco_term = 4
elif vendor_inco_term == 'DAP':
    vendor_inco_term = 2
else:
    vendor_inco_term = 0

if shipment_mode == 'Air':
    shipment_mode = 0
elif shipment_mode == 'Truck':
    shipment_mode = 4
elif shipment_mode == 'Air Charter':
    shipment_mode = 1
elif shipment_mode == 'Other':
    shipment_mode = 3
else:
    shipment_mode = 2

if product_group == 'ARV':
    product_group = 2
elif product_group == 'HRDT':
    product_group = 3
elif product_group == 'ANTM':
    product_group = 1
elif product_group == 'ACT':
    product_group = 0
else:
    product_group = 4

if subclassification == 'Adult':
    subclassification = 1
elif subclassification == 'Pediatric':
    subclassification = 5
elif subclassification == 'HIV test':
    subclassification = 2
elif subclassification == 'HIV test - Ancillary':
    subclassification = 3
elif subclassification == 'Malaria':
    subclassification = 4
else:
    subclassification = 0

if designation == 'Yes':
    designation = 1
else:
    designation = 0



data_1 = [po_so, asn_dn, managed_by, fullfill_via, vendor_inco_term, shipment_mode, product_group, subclassification, designation]
data_2 = [weight, freight_cost]
data_2 = np.reshape(data_2, (1, -1))
data_2 = scaler.transform(data_2)
list_1 = []
for i in data_2:
    for j in i:
        list_1.append(j)


data = data_1 + list_1
data = np.reshape(data, (1, -1))
prediction = model.predict(data)

submit = st.button('Predict')
if submit:
    st.write('Consignment Price is $',prediction[0])
