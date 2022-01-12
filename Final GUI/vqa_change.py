##############################################
#
#USE model_vqa_vgg19_5layers FOR THE MODEL CREATED IN COLLEGE
#USE model_vqa_VGG19 FOR THE MODEL THAT WAS SEND WITH THE CODE
#
###############################################
import warnings
warnings.filterwarnings("ignore")
import os, argparse
import keras, cv2, spacy, numpy as np
from keras.models import model_from_json, Model, Sequential, load_model
from keras.optimizers import SGD
from sklearn.externals import joblib
from keras import backend as K
from keras.utils.vis_utils import plot_model
from keras.applications.vgg19 import VGG19  
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input, decode_predictions
from keras.layers.core import Reshape, Activation, Dropout
from keras.layers import LSTM, Dense, Concatenate, Input
from keras.metrics import top_k_categorical_accuracy
import json

word_embeddings = spacy.load('en_vectors_web_lg')
#VQA_weights_file_name   = 'model_vqa_vgg19.h5'
label_encoder_file_name = 'FULL_labelencoder_trainval.pkl'

model_vgg = VGG19(include_top=True)
model_vgg = Model(inputs=model_vgg.input, outputs=model_vgg.get_layer('fc2').output)
model_vgg.summary()

def top_3_accuracy(y,z):
	return top_k_categorical_accuracy(y,z,k=3)

def get_image_features(image_file_name):
    img_path = image_file_name
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model_vgg.predict(x)
    return features
    
def get_question_features(question):
    tokens = word_embeddings(question)
    question_tensor = np.zeros((1, 30, 300))
    for j in range(len(tokens)):
        question_tensor[0,j,:] = tokens[j].vector
    return question_tensor
	


json_file = open('model_vqa_vgg19_5layers.json', 'r')
#json_file = open('model_vqa_VGG19.json', 'r')


loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)


loaded_model.load_weights("model_vqa_vgg19_5layers.h5")
#loaded_model.load_weights("model_vqa_VGG19.h5")


print("Loaded model from disk")
#model_vga = load_model('model_vqa_vgg19_5layers.h5',custom_objects={'top_3_accuracy':top_3_accuracy})
loaded_model.summary()
labelencoder = joblib.load(label_encoder_file_name)

def run_func(question,filename):
    resultset=[]
    image_file_name = filename
    image_features = get_image_features(image_file_name)
    print('img')
    question_features = get_question_features(question)
    print('question')
    y_output = loaded_model.predict([question_features, image_features])
    warnings.filterwarnings("ignore", category=DeprecationWarning)
#print(y_output[0])
    for label in reversed(np.argsort(y_output)[0,-5:]):
        print (str(round(y_output[0,label]*100,2)).zfill(5), "% ",labelencoder.classes_[label])
        resultset.append(tuple((labelencoder.classes_[label], round(y_output[0,label]*100,2))))
    return resultset


