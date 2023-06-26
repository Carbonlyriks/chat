
# import sklearn
import pickle , numpy as np
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
model = pickle.load(open(r"C:/Users/Ashok_sha/Downloads/trained_SVM_model.sav",'rb'))
# scaler.transform()
def process_inputData(data):
    # changing the input data to numpy_array
    input_data=np.asarray(data)

    # reshape the array as 
    input_data_reshaped = input_data.reshape(1,-1)

    # standardized the input data
    scaler.fit(input_data_reshaped)
    std_input=scaler.transform(input_data_reshaped)
    return(std_input)
def report(predict):
    print(f"Person is {'Not Diabetic' if predict[0]==0 else 'Diabetic'}")
   
# sam = [2,197,70,45,543,30.5,0.158,53]
sam1=[8,99,84,0,0,35.4,0.388,50]

 
std_input = process_inputData(sam1)

# # predict 
# # svm_Predict=classifier.predict(std_input)
LoReg_predict=model.predict(std_input)
report(LoReg_predict)


