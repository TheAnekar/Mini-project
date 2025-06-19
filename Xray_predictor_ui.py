import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import os
import subprocess
import math

class MRIClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RespireX | MRI Scan Classifier")
        self.root.geometry("1100x700")
        self.root.configure(bg="#111")

        self.class_names = ['Benign', 'Malignant', 'Normal']
        self.image_path = None
        self.model = None

        try:
            self.model = tf.keras.models.load_model("my_model.keras")
        except Exception as e:
            messagebox.showerror("Model Load Error", str(e))

        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#111")
        header.pack(fill="x", pady=5)
        back_btn = tk.Label(header, text="← Back to Dashboard", font=("Orbitron", 10), fg="#00f6ff", bg="#111", cursor="hand2")
        back_btn.pack(side="left", padx=10)
        back_btn.bind("<Button-1>", self.go_back_to_dashboard)

        title = tk.Label(header, text="MRI Scan Classifier", font=("Orbitron", 20, "bold"), fg="#00f6ff", bg="#111")
        title.pack(pady=5)

        content = tk.Frame(self.root, bg="#111")
        content.pack(fill="both", expand=True)

        # Left Panel - Image
        self.left_panel = tk.Frame(content, bg="#111")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        self.preview_panel = tk.Label(self.left_panel, bg="#111")
        self.preview_panel.pack(pady=10)

        self.image_info_label = tk.Label(self.left_panel, text="", fg="white", bg="#111", font=("Orbitron", 10))
        self.image_info_label.pack(pady=5)

        btn_frame = tk.Frame(self.left_panel, bg="#111")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Upload MRI Image", font=("Orbitron", 12), bg="#222", fg="#00f6ff",
                  relief="flat", command=self.upload_image).pack(side='left', padx=10)

        tk.Button(btn_frame, text="Clear Image", font=("Orbitron", 12), bg="#222", fg="#00f6ff",
                  relief="flat", command=self.clear_image).pack(side='left', padx=10)

        # Right Panel - Prediction
        self.right_panel = tk.Frame(content, bg="#111")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        self.result_title = tk.Label(self.right_panel, text="Prediction Results", font=("Orbitron", 16, "bold"), fg="#00f6ff", bg="#111")
        self.result_title.pack(pady=10)

        self.progress_bars = {}
        for cls in self.class_names:
            lbl = tk.Label(self.right_panel, text=cls, font=("Orbitron", 10), fg="white", bg="#111")
            lbl.pack(anchor="w", padx=5)
            bar = ttk.Progressbar(self.right_panel, length=300, mode="determinate")
            bar.pack(pady=2)
            self.progress_bars[cls] = bar

        self.top_result = tk.Label(self.right_panel, text="", font=("Orbitron", 14, "bold"), fg="#00f6ff", bg="#111")
        self.top_result.pack(pady=15)

        self.predict_btn = tk.Button(self.right_panel, text="Predict", font=("Orbitron", 12), bg="#222", fg="#00f6ff",
                                     relief="flat", command=self.predict)
        self.predict_btn.pack(pady=10)

    def go_back_to_dashboard(self, *_):
        self.root.destroy()
        subprocess.Popen(["python3", "app.py"])

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not path:
            return

        self.image_path = path
        img = Image.open(path).resize((224, 224))
        self.img_tk = ImageTk.PhotoImage(img)
        self.preview_panel.config(image=self.img_tk)

        file_info = os.stat(path)
        size_kb = math.ceil(file_info.st_size / 1024)
        file_name = os.path.basename(path)
        file_type = os.path.splitext(path)[1].upper().replace(".", "")

        self.image_info_label.config(
            text=f"File: {file_name}\nType: {file_type} | Size: {size_kb} KB | Resolution: 224x224")

        self.top_result.config(text="")
        for bar in self.progress_bars.values():
            bar["value"] = 0

    def clear_image(self):
        self.image_path = None
        self.preview_panel.config(image="")
        self.image_info_label.config(text="")
        self.top_result.config(text="")
        for bar in self.progress_bars.values():
            bar["value"] = 0

    def predict(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return

        if not self.model:
            messagebox.showerror("Model Error", "Model not loaded.")
            return

        try:
            img = Image.open(self.image_path).resize((224, 224)).convert("RGB")
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            prediction = self.model.predict(img_array)[0]

            top_index = np.argmax(prediction)
            top_class = self.class_names[top_index]
            top_conf = prediction[top_index] * 100

            for i, cls in enumerate(self.class_names):
                conf = prediction[i] * 100
                self.progress_bars[cls]["value"] = conf

            color = "#00ff88" if top_class == "Normal" else ("#ffe266" if top_class == "Benign" else "#ff4c4c")
            self.top_result.config(text=f"{top_class} ({top_conf:.2f}%)", fg=color)

        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = MRIClassifierApp(root)
    root.mainloop()
