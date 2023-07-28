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

class Sentiment:
    def __init__(self,data):
        self.data = np.array(data)
        self.model = None
        self.result = None

    def load_model(self,model_dir = os.path.join('utils','model_sentiment_LSTM.h5'), weight_dir = os.path.join('utils','weights_sentiment_LSTM.h5')):
        self.model = load_model(model_dir, compile=False )
        self.model.load_weights(weight_dir)

    def inference(self):
        with open(os.path.join('utils','tokenizer.pickle'), 'rb') as handle:
            tokenizer = pickle.load(handle)
        
        # Model configuration
        vocab_size = 20000
        embedding_dim = 16
        max_length = 20
        trunc_type = 'post'
        padding_type = 'post'
        oov_tok = "<OOV>"

        #Inference process
        sequences = tokenizer.texts_to_sequences(self.data)
        
        padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
        self.result = np.rint(self.model.predict(padded)).flatten()

    def export_inference(self):
        result = self.result.flatten()
        result = self.result.astype(int)
        result = result.tolist()
        return result

    def debug(self):
        print(self.result)