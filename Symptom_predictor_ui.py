import tkinter as tk
from tkinter import messagebox
import pickle
import numpy as np
from PIL import Image, ImageTk
import urllib.request
import io
import subprocess
import csv
import os


class SymptomPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RespireX | Symptom-Based Prediction")
        self.root.geometry("1000x700")
        self.root.configure(bg="#111")

                # ✅ Back to Dashboard Navigation
        header = tk.Frame(self.root, bg="#111")
        header.pack(fill="x", pady=5)
        back_label = tk.Label(header, text="← Back to Dashboard", font=("Orbitron", 10),
                              fg="#00f6ff", bg="#111", cursor="hand2")
        back_label.pack(side="left", padx=10)
        back_label.bind("<Button-1>", self.go_back_to_dashboard)

        # Load model and scaler
        try:
            with open("model.pkl", "rb") as f:
                self.scaler, self.model = pickle.load(f)
        except Exception as e:
            messagebox.showerror("Model Load Error", str(e))
            self.scaler = None
            self.model = None

        # Card content
        self.info_cards = [
            {"title": "Coughing of Blood", "text": "Coughing up blood (hemoptysis) is a red flag symptom often associated with lung cancer. It typically occurs when tumors erode nearby blood vessels in the airways, causing bleeding. Although it can also occur in infections or bronchitis, its presence in smokers or high-risk patients is taken very seriously in predictive modeling. Its rarity in benign conditions makes it a high-weight factor."},
            {"title": "Chest Pain", "text": "Persistent chest pain, particularly when breathing or coughing, may indicate tumor pressure or invasion into the chest wall or pleura. This symptom is more predictive when it occurs alongside shortness of breath or coughing of blood. While pain can stem from many causes, its chronic and localized form is significant in lung cancer diagnosis models."},
            {"title": "Weight Loss", "text": "Unexplained weight loss is often an early systemic sign of cancer, including lung cancer. Tumors can cause metabolic changes that burn calories rapidly, even when the patient is not trying to lose weight. In prediction models, sudden weight loss can elevate risk even if other symptoms appear mild."},
            {"title": "Shortness of Breath", "text": "Shortness of breath (dyspnea) is a common symptom caused by airway obstruction, fluid buildup, or reduced lung capacity due to tumors. Its onset—especially in non-asthmatic patients—can be an early indicator of pulmonary compromise, adding weight in lung cancer prediction algorithms."},
            {"title": "Smoking", "text": "Smoking is the single most significant risk factor for lung cancer. Tobacco smoke contains carcinogens that directly damage lung tissue over time. Prediction models treat heavy smoking history as a dominant feature. Even moderate smoking increases risk sharply when combined with other symptoms."},
            {"title": "Genetic Risk", "text": "Family history and inherited genetic mutations can predispose individuals to lung cancer even without environmental exposures. In models, genetic risk adds predictive value when combined with factors like smoking and environmental pollution."},
            {"title": "Wheezing", "text": "Wheezing occurs when airflow through the lungs is restricted, often by narrowed airways or tumor growth. While also common in asthma or infections, new or worsening wheezing in older adults may signal lung abnormalities. Its context is key in prediction."},
            {"title": "Fatigue", "text": "Chronic fatigue can indicate systemic cancer-related changes. While non-specific, when paired with other symptoms, fatigue can signal the body’s immune response to tumor presence. It's a supportive but important predictive feature."},
            {"title": "Air Pollution", "text": "Exposure to air pollution, especially in urban or industrial environments, increases lung cancer risk over time. Pollutants like PM2.5 particles and toxic gases damage lung cells and contribute to inflammation. Prediction models treat long-term pollution exposure as an environmental risk marker."},
            {"title": "Passive Smoker", "text": "Passive or second-hand smoke exposure can cause similar cellular damage as active smoking. Non-smokers living with smokers or working in smoky environments often face elevated risks. This factor is crucial in detecting high-risk non-smokers in machine learning models."}
        ]
        self.current_card = 0

        self.create_info_card_ui()
        self.create_prediction_ui()

        # Start card auto-rotation
        self.root.after(30000, self.auto_rotate_card)

    def create_info_card_ui(self):
        wrapper = tk.Frame(self.root, bg="#111")
        wrapper.pack(pady=20, fill='x')

        self.left_btn = tk.Button(wrapper, text="←", font=("Orbitron", 14), width=4, bg="#111", borderwidth=0,
                                   fg="#00f6ff", activebackground="#111", relief="flat",
                                   command=self.prev_card)
        self.left_btn.pack(side='left', padx=5)

        self.card_frame = tk.Frame(wrapper, bg="#1c1c1c", highlightbackground="#1c1c1c", highlightthickness=0)
        self.card_frame.pack(side='left', expand=True, fill='both')

        self.card_title = tk.Label(self.card_frame, text="", font=("Orbitron", 14, "bold"), fg="#00f6ff", bg="#1c1c1c")
        self.card_title.pack(pady=10)

        self.card_text = tk.Label(self.card_frame, text="", font=("Orbitron", 10), fg="white", bg="#1c1c1c",
                                  wraplength=700, justify='left')
        self.card_text.pack(padx=10, pady=10)

        self.right_btn = tk.Button(wrapper, text="→", font=("Orbitron", 14), width=4, bg="#111", borderwidth=0,
                                    fg="#00f6ff", activebackground="#111", relief="flat",
                                    command=self.next_card)
        self.right_btn.pack(side='left', padx=5)

        self.display_card(0)

    def display_card(self, index):
        card = self.info_cards[index]
        self.card_title.config(text=card['title'])
        self.card_text.config(text=card['text'])

    def next_card(self):
        self.current_card = (self.current_card + 1) % len(self.info_cards)
        self.display_card(self.current_card)

    def prev_card(self):
        self.current_card = (self.current_card - 1) % len(self.info_cards)
        self.display_card(self.current_card)

    def auto_rotate_card(self):
        self.next_card()
        self.root.after(30000, self.auto_rotate_card)

    def create_prediction_ui(self):
        form_frame = tk.Frame(self.root, bg="#111")
        form_frame.pack(pady=10)

        self.features = [
            "Coughing of Blood", "Chest Pain", "Weight Loss", "Shortness of Breath",
            "Smoking", "Genetic Risk", "Wheezing", "Fatigue", "Air Pollution", "Passive Smoker"
        ]
        self.entries = {}

        for feature in self.features:
            row = tk.Frame(form_frame, bg="#111")
            row.pack(fill='x', pady=2)
            lbl = tk.Label(row, text=feature, bg="#111", fg="white", width=25, anchor='w', font=("Orbitron", 10))
            lbl.pack(side='left', padx=5)
            entry = tk.Entry(row, bg="#222", fg="white", insertbackground='white', relief='flat', width=10)
            entry.pack(side='left')
            self.entries[feature] = entry

        btn_frame = tk.Frame(self.root, bg="#111")
        btn_frame.pack(pady=15)

        self.predict_btn = tk.Button(btn_frame, text="Predict", font=("Orbitron", 12, "bold"),
                                     bg="#222", fg="#00f6ff", relief="flat",
                                     activebackground="#333", activeforeground="#00f6ff",
                                     command=self.predict)
        self.predict_btn.pack(side='left', padx=10, ipadx=10, ipady=5)

        self.reset_btn = tk.Button(btn_frame, text="Reset", font=("Orbitron", 12, "bold"),
                                     bg="#222", fg="#00f6ff", relief="flat",
                                     activebackground="#333", activeforeground="#00f6ff",
                                     command=self.reset_fields)
        self.reset_btn.pack(side='left', padx=10, ipadx=10, ipady=5)

        self.result_label = tk.Label(self.root, text="", font=("Orbitron", 12), fg="#00f6ff", bg="#111")
        self.result_label.pack(pady=10)

    def reset_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.result_label.config(text="")

    def predict(self):
        if not self.model or not self.scaler:
            messagebox.showerror("Model Error", "Model or scaler not loaded.")
            return

        try:
            values = []
            for feature in self.features:
                val = self.entries[feature].get().strip()
                try:
                    num = int(val)
                    if not (0 <= num <= 9):
                        raise ValueError
                    values.append(num)
                except:
                    raise ValueError(f"Invalid input for {feature}. Enter a whole number between 0–9.")
            

            features_scaled = self.scaler.transform([values])
            pred = self.model.predict(features_scaled)[0]
            risk_mapping = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
            color = {"Low Risk": "#00ff88", "Medium Risk": "#ffe266", "High Risk": "#ff4c4c"}
            result = risk_mapping.get(pred, "Unknown")

            self.result_label.config(text=f"Predicted Risk: {result}", fg=color.get(result, "white"))

        # ✅ Log to CSV
            import csv, os
            log_file = "prediction_log.csv"
            fields = self.features + ["Predicted Risk"]
            row = values + [result]
            file_exists = os.path.isfile(log_file)
            with open(log_file, mode='a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(fields)
                writer.writerow(row)

        # ✅ Clear fields after prediction
            for entry in self.entries.values():
                entry.delete(0, tk.END)

        except ValueError as ve:
            messagebox.showwarning("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    def go_back_to_dashboard(self, *_):
        self.root.destroy()
        subprocess.Popen(["python3", "app.py"])


if __name__ == "__main__":
    root = tk.Tk()
    app = SymptomPredictorApp(root)
    root.mainloop()

