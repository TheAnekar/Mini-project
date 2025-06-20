import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ----------- Step 1: Set Dataset Paths ----------- #
# Make sure the directory structure is like:
# /lung_cancer_MRI_dataset/train/
# /lung_cancer_MRI_dataset/validate/

dataset_root = '/lung_cancer_MRI_dataset'
train_dir = 'lung_cancer_MRI_dataset/train'
val_dir = 'lung_cancer_MRI_dataset/validate'

# ----------- Step 2: Image Data Preprocessing ----------- #
img_size = (224, 224)
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

# ----------- Step 3: Build the Model ----------- #
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze feature extractor

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# ----------- Step 4: Compile ----------- #
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# ----------- Step 5: Train ----------- #
epochs = 10
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    validation_data=val_generator,
    validation_steps=val_generator.samples // batch_size,
    epochs=epochs
)

# ----------- Step 6: Evaluate ----------- #
loss, accuracy = model.evaluate(val_generator)
print(f"\n🎯 Validation Accuracy: {accuracy * 100:.2f}%")

# ----------- Step 7: Save Model ----------- #
model.save('lung_cancer_model.keras')
print("💾 Model saved as 'lung_cancer_model.keras'")
