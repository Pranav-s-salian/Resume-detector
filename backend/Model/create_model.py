from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout, BatchNormalization




def create_model(vocab_size=15000, max_length=500, num_classes=25, embedding_dim=128):
    print("this will be creting an BiRnn model")
    model = Sequential([
       
        Embedding(
            input_dim=vocab_size, 
            output_dim=embedding_dim, 
            input_length=max_length,
            name='embedding'
        ),
        
        
        Bidirectional(
            LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.3), ## here we are addingdropout to prevent from overfitting, and recureent droppout to prevent the memory of lstm to not store it, 
            name='bilstm_1'
        ),
    
        Bidirectional(
            LSTM(64, return_sequences=False, dropout=0.3, recurrent_dropout=0.3), ## here also same 
            name='bilstm_2'
        ),
        
        
        Dense(256, activation='relu', name='dense_1'),  ##this is the frist nueron layer with 256 nuerons, with batch normalization to imporove its stabilty
        BatchNormalization(name='batch_norm_1'),
        Dropout(0.5, name='dropout_1'),
        
        # Second dense layer
        Dense(128, activation='relu', name='dense_2'),
        BatchNormalization(name='batch_norm_2'),
        Dropout(0.4, name='dropout_2'),
        
        # Third dense layer
        Dense(64, activation='relu', name='dense_3'),
        Dropout(0.3, name='dropout_3'),
        
        # Fourth dense layer
        Dense(32, activation='relu', name='dense_4'),
        Dropout(0.2, name='dropout_4'),
        
        # Output layer
        Dense(num_classes, activation='softmax', name='output')
    ])
    
    
    model.compile(
        loss='sparse_categorical_crossentropy', ##compiling the mdoelk with multi class classification 
        optimizer='adam',
        metrics=['accuracy']
    )
    
    print("Model architecture:")
   
    
    return model, model.summary()  #return this model, and its architecture details 