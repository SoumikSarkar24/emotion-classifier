import os
import numpy as np
import tensorflow as tf
import gradio as gr

# Load the trained model
model = tf.keras.models.load_model("image_classifier.keras")

def predict_emotion(img):
    if img is None:
        return "Please upload an image."

    # Resize image
    img_resized = tf.image.resize(img, (128, 128))

    # Add batch dimension
    img_batch = np.expand_dims(img_resized, axis=0)

    # Predict
    score = model.predict(img_batch, verbose=0)[0][0]

    # Happy = 0, Sad = 1
    if score >= 0.5:
        emotion = "Sad 😢"
        confidence = score * 100
    else:
        emotion = "Happy 😊"
        confidence = (1 - score) * 100

    return f"{emotion} ({confidence:.2f}% Confidence)"

demo = gr.Interface(
    fn=predict_emotion,
    inputs=gr.Image(type="numpy"),
    outputs=gr.Textbox(label="Prediction"),
    title="Emotion Classifier (Happy vs. Sad)",
    description="Upload a face image to predict whether the emotion is Happy or Sad."
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)