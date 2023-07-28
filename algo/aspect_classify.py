import tensorflow as tf
import pickle
import os
import numpy as np
import json
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Nadam
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences



class Classify:
    def __init__(self, data):
        self.data = np.array(data)
        self.parameter = None
        self.model = None
        self.result = None

    def preprocessing(self):
        with open(os.path.join('utils','tokenizer.pickle'), 'rb') as handle:
            tokenizer = pickle.load(handle)

        #inisiasi variabel klasifikasi
        arr = []
        

        for x in self.data:
            meta_aspect = self.toJSON(x['meta_aspect'])
            meta_opinion = self.toJSON(x['meta_opinion'])

            row_input = []

            aspect_json_lemma = tokenizer.texts_to_sequences([meta_aspect['lemma']])[0][0]
            aspect_json_upos = tokenizer.texts_to_sequences([meta_aspect['upos']])[0][0]
            aspect_json_xpos = tokenizer.texts_to_sequences([meta_aspect['xpos']])[0][0]
            opini_json_lemma = tokenizer.texts_to_sequences([meta_opinion['lemma']])[0][0]
            opini_json_upos = tokenizer.texts_to_sequences([meta_opinion['upos']])[0][0]
            opini_json_xpos = tokenizer.texts_to_sequences([meta_opinion['xpos']])[0][0]
            opini_json_deprel = tokenizer.texts_to_sequences([meta_opinion['deprel']])[0][0]

            row_input.extend([aspect_json_lemma, aspect_json_upos, aspect_json_xpos])
            row_input.extend([opini_json_lemma, opini_json_upos, opini_json_xpos, opini_json_deprel])
            arr.append(row_input)
        
        self.parameter = np.array(arr)

    
    def load_model(self):
        tf.keras.utils.get_custom_objects()['Nadam'] = Nadam
        self.model = load_model(os.path.join('utils','model_lstm.h5'), compile=False )
        self.model.load_weights(os.path.join('utils','weights_lstm.h5'))


    def inference(self):
        self.result = self.model.predict(self.parameter)

    def export_inference(self):
        result = self.result.flatten()
        result = result.astype(int)
        result = result.tolist()
        return result

    def debug(self):
        if self.result is not None:
            print(self.result)

    
        

    
    def toJSON(self,word):
        jsonn = word.replace("'", "\"")
        return json.loads(jsonn)
