from keras.models import Model
from keras.layers import Input, Dense
from keras.optimizers import Adam


def get_model(input_shape, hyperspace):
    
    inputs = Input(shape=input_shape)
    
    layer = Dense(130, activation='relu')(inputs)
    layer = Dense(90, activation='relu')(layer)
    if hyperspace['hidden_layers'] == 3:
        layer = Dense(50, activation='relu')(layer)
    output = Dense(5, activation='relu')(layer)
   
    model = Model(inputs=inputs, outputs=output)
   
    model.compile(loss="mse",optimizer=Adam(hyperspace['lr'], decay=hyperspace['decay']))
    
    return model