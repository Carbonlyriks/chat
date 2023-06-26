# import sklearn
import pickle , numpy as np
from sklearn.preprocessing import StandardScaler
import streamlit as st

# load model
scaler = StandardScaler()
model = pickle.load(open(r"C:/Users/Ashok_sha/Downloads/trained_SVM_model.sav",'rb'))


#creating funtion for prediction
def diabetes_prediction(data):
    # changing the input data to numpy_array
    input_data=np.asarray(data)

    # reshape the array as 
    input_data_reshaped = input_data.reshape(1,-1)

    # standardized the input data
    scaler.fit(input_data_reshaped)
    std_input=scaler.transform(input_data_reshaped)
    prediction = model.predict(std_input)
    return print(f"Person is {'Not Diabetic' if prediction[0]==0 else 'Diabetic'}")




sam = [4,125,70,18,122,28.9,1.144,45]
sam1=[8,99,84,0,0,35.4,0.388,50]

diabetes_prediction(sam1)
diabetes_prediction(sam)

