# RespireX - Lung Cancer Detection and Prediction

**RespireX** is an AI-powered application designed for early detection and prediction of lung cancer. It combines image and text-based deep learning models to provide accurate results and a user-friendly interface.

---

## 🩺 Features

* **Lung Cancer Detection**: Detects malignant and benign lung conditions from CT scan images using a deep learning model.
* **Prediction from Reports**: Analyzes patient reports using a separate AI model for prediction.
* **Interactive UI**: Modern and responsive interface for smooth user experience.

---

## 💻 Technologies Used

* **Frontend**: PyQt5, Tkinter
* **Backend**: Python, Flask
* **AI/ML**: TensorFlow/Keras for image and text models
* **Other Libraries**: OpenCV, NumPy, Pandas, Flask

---

## 🚀 Installation

1. **Clone the repository**

```bash
git clone https://github.com/TheAnekar/Mini-project
cd Mini-project
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```

5. **Open in Browser**
   Go to `http://127.0.0.1:5000` to access RespireX.

---

## 🧠 Model Integration

* **Image Model**: `lung_cancer_model.keras`
  Processes CT scan images and classifies them as benign or malignant.

* **Text Model**: `model.pkl`
  Predicts lung cancer risk from patient medical reports.

---

## ⚡ Usage

1. Upload a lung CT scan image or enter a patient report.
2. Get real-time predictions for lung cancer detection.

---

## 📈 Future Enhancements

* Improve model accuracy with larger datasets.
* Add real-time chat support for patients.
* Integrate cloud-based deployment for global access.

---

## 💡 Contact

**Harris Ruben**
* Email: [harrisrubenr.com](mailto:harrisrubenr.com)
* GitHub: [https://github.com/harrisruben](https://github.com/harrisruben)
---
**Mohamed Ashraf**
* Email: [iamashraf28.com](mailto:iamashraf28.com)
* GitHub: [https://github.com/harrisruben](https://github.com/TheAnekar)
