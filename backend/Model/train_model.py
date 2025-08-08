from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
import datetime
import os


def train_model(model, X_train, X_test, y_train, y_test, epochs=20, batch_size=32):
   
    print("\n🔹 Setting up callbacks...")
    
    
    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    os.makedirs(log_dir, exist_ok=True)
    
    
    tensorboard_cb = TensorBoard(
        log_dir=log_dir, 
        histogram_freq=1,
        write_graph=True,
        update_freq='epoch'
    )
    
    early_stopping_cb = EarlyStopping(
        monitor='val_loss', 
        patience=5, 
        restore_best_weights=True,
        verbose=1
    )
    
    checkpoint_cb = ModelCheckpoint(
        "best_model.h5", 
        monitor='val_accuracy', 
        save_best_only=True,
        verbose=1,
        mode='max'
    )
    
    
    from tensorflow.keras.callbacks import ReduceLROnPlateau
    lr_reducer = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
    
    callbacks = [tensorboard_cb, early_stopping_cb, checkpoint_cb, lr_reducer]
    
    print(f"\n🔹 Training model for {epochs} epochs...")
    print(f"Batch size: {batch_size}")
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_test)}")
    
    # Train model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    return history