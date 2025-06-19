import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import urllib.request, io, subprocess

import random

# ---------- Theme Colors ----------
BG_DARK = "#111"
FG_NEON = "#00f6ff"
FG_TEXT = "#ffffff"

# ---------- Content Sections ----------

CONTENT_SECTIONS = [
    ("Why Screening Matters",
     "The American Cancer Society recommends annual low-dose CT (LDCT) screening for adults aged 50 to 80 who have a 20 pack-year smoking history and currently smoke or have quit within the past 15 years. LDCT can detect lung tumors long before symptoms arise. Early detection through LDCT has been shown to reduce lung cancer mortality by approximately 20%, making it one of the most effective tools in saving lives from lung cancer."),

    ("Doctor Insight",
     "“Unfortunately, when tumors grow within our lungs, it's not something our bodies can sense or feel. So we miss it at its earliest stages, unless we screen.” — Dr. Mansfield\n\n“Patients should talk to their primary-care provider about lung-cancer screening, especially if they have any history of smoking. The earlier we find it, the more options we have for treatment.” — Dr. Swanson, Mayo Clinic"),

    ("Risk Isn’t Only Smoking",
     "While cigarette smoking remains the leading cause of lung cancer, accounting for more than 80% of cases, other factors contribute significantly to risk. Prolonged exposure to second-hand smoke, air pollution, radon gas, and occupational carcinogens like asbestos and diesel exhaust also increase lung cancer risk. Genetic predisposition and family history are also key considerations. Recognizing non-smoking-related risks is critical to identifying vulnerable individuals who might otherwise be overlooked."),

    ("Understanding Lung Cancer",
     "Lung cancer is a disease characterized by uncontrolled cell growth in the lung tissues. If untreated, it can metastasize to nearby tissues or other parts of the body. It is one of the most common and deadly cancers worldwide, primarily because it is often diagnosed at an advanced stage. Tumors can obstruct airways or invade vital structures, making early intervention crucial. This complexity requires multidisciplinary management and heightened public awareness for better outcomes."),

    ("Types of Lung Cancer",
     "Lung cancer is broadly classified into two types: Non-small cell lung cancer (NSCLC) and Small cell lung cancer (SCLC). NSCLC accounts for about 85% of cases and includes subtypes like adenocarcinoma, squamous cell carcinoma, and large cell carcinoma. SCLC, though less common, is more aggressive and rapidly growing. It is often diagnosed after it has already spread. Understanding the type of cancer influences treatment decisions, response to therapy, and prognosis."),

    ("Common Causes",
     "Smoking is the most significant risk factor, but lung cancer can also be caused by long-term exposure to harmful substances. Radon, a naturally occurring radioactive gas, is the second-leading cause of lung cancer in the U.S. Occupational exposures to carcinogens such as asbestos, arsenic, chromium, and nickel also increase risk. Environmental pollution, especially fine particulate matter in urban areas, can further contribute."),

    ("Symptoms to Watch",
     "Early lung cancer often presents with minimal or no symptoms, but as it progresses, common symptoms may include a persistent cough, coughing up blood, chest pain, shortness of breath, wheezing, hoarseness, unexplained weight loss, fatigue, and recurrent respiratory infections. Because these symptoms overlap with other respiratory conditions, they are often dismissed."),

    ("How Lung Cancer is Diagnosed",
     "Diagnosis typically starts with imaging tests like chest X-rays and CT scans. If a suspicious lesion is found, a biopsy is performed—often via bronchoscopy, needle aspiration, or surgical methods—to obtain a tissue sample for pathological analysis. PET scans, MRI, and blood work may follow to assess spread and determine the cancer’s stage."),

    ("Stages of Lung Cancer",
     "Staging ranges from Stage 0 (in-situ) to Stage IV (metastatic). Stage I cancers may be treated surgically, while advanced stages require chemotherapy, radiation, or immunotherapy. Staging helps guide treatment plans and predicts outcomes."),

    ("Fatality Rates and Survival",
     "Lung cancer has one of the highest cancer mortality rates. However, the 5-year survival rate improves dramatically with early detection. Localized cancers have survival rates over 60%, while late-stage cancers are closer to 5–10%. Advances in treatment continue to improve these odds."),

    ("Treatment Options",
     "Treatment may involve surgery, chemotherapy, radiation, targeted drugs, immunotherapy, or a combination. Decisions depend on cancer type, location, stage, and patient health. Modern approaches increasingly use precision medicine based on genetic markers."),

    ("Living with Lung Cancer",
     "Supportive care is essential. Many people continue to live meaningful lives after diagnosis. Support groups, physical therapy, palliative care, and mental health services all help improve quality of life throughout treatment and survivorship.")
]

# ---------- Collapsible Section Widget ----------
class CollapsibleSection(tk.Frame):
    def __init__(self, parent, title, content, expanded=False):
        super().__init__(parent, bg=BG_DARK)
        self.title = title
        self.content = content
        self.expanded = expanded

        self.toggle_btn = tk.Button(
            self, text=f"▼ {title}" if expanded else f"▶ {title}",
            font=("Orbitron", 12, "bold"), bg="#222", fg=FG_NEON,
            anchor="w", relief="flat", command=self.toggle
        )
        self.toggle_btn.pack(fill="x", padx=10, pady=2)

        self.body = tk.Label(
            self, text=content, wraplength=900, justify="left",
            font=("Orbitron", 10), fg=FG_TEXT, bg=BG_DARK
        )

        if expanded:
            self.body.pack(fill="x", padx=20, pady=5)

    def toggle(self):
        if self.expanded:
            self.body.pack_forget()
            self.toggle_btn.config(text=f"▶ {self.title}")
        else:
            self.body.pack(fill="x", padx=20, pady=5)
            self.toggle_btn.config(text=f"▼ {self.title}")
        self.expanded = not self.expanded

# ---------- Dashboard Class ----------
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("RespireX | Dashboard")
        self.root.geometry("1280x800")
        self.dark_mode = True
        self.fullscreen = False

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        self.root.configure(bg=BG_DARK)

        # Header
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", pady=2)
        tk.Label(header, text="🫁 RespireX", font=("Orbitron", 20, "bold"),
                 bg=BG_DARK, fg=FG_NEON).pack(side="left", padx=10)

        self.breadcrumb = tk.Label(header, text="Home ▸ Dashboard",
                                   font=("Orbitron", 10), bg=BG_DARK, fg=FG_NEON)
        self.breadcrumb.pack(side="left", padx=10)

        # Search bar
        self.search_var = tk.StringVar()
        tk.Entry(header, textvariable=self.search_var, width=20, bg="#222", fg=FG_TEXT,
                 insertbackground=FG_TEXT, relief="flat", font=("Orbitron", 10)).pack(side="right", padx=5)
        tk.Button(header, text="🔍", command=self._run_search, bg="#222", fg=FG_NEON, relief="flat").pack(side="right")

        # Sitemap & theme
        tk.Button(header, text="☾", bg="#222", fg=FG_NEON, relief="flat",
                  command=self._toggle_theme).pack(side="right", padx=5)
        tk.Button(header, text="🗺", bg="#222", fg=FG_NEON, relief="flat",
                  command=self._show_sitemap).pack(side="right")

        # Sidebar
        sidebar = tk.Frame(self.root, bg=BG_DARK, width=200)
        sidebar.pack(side="left", fill="y")

        tk.Button(sidebar, text="🏠  Dashboard", font=("Orbitron", 10), bg="#222",
                  fg=FG_NEON, relief="flat").pack(fill="x", pady=4, padx=5)
        tk.Button(sidebar, text="🩺  Symptoms Predictor", font=("Orbitron", 10), bg="#222",
                  fg=FG_NEON, relief="flat", command=self._launch_symptom).pack(fill="x", pady=4, padx=5)
        tk.Button(sidebar, text="🧠  MRI Classifier", font=("Orbitron", 10), bg="#222",
                  fg=FG_NEON, relief="flat", command=self._launch_mri).pack(fill="x", pady=4, padx=5)

        # Scrollable main content
        main = tk.Frame(self.root, bg=BG_DARK)
        main.pack(side="left", fill="both", expand=True)

        canvas = tk.Canvas(main, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
        self.content_frame = tk.Frame(canvas, bg=BG_DARK)

        self.content_frame.bind("<Configure>",
                                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas = canvas

        self._build_banner()
        self._build_buttons()
        self._build_collapsible_sections()

    def _build_banner(self):
        try:
            url = "https://img.freepik.com/premium-photo/virtual-human-lungs-dark-blue-background-low-poly.jpg"
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            image = Image.open(io.BytesIO(raw_data))
            image = image.resize((600, 250))
            self.banner_img = ImageTk.PhotoImage(image)
            tk.Label(self.content_frame, image=self.banner_img, bg=BG_DARK).pack(pady=10)
        except Exception:
            pass

        tk.Label(self.content_frame, text="Lung Cancer Detection & Education Hub",
                 font=("Orbitron", 16, "bold"), fg=FG_NEON, bg=BG_DARK).pack(pady=10)

    def _build_buttons(self):
        wrap = tk.Frame(self.content_frame, bg=BG_DARK)
        wrap.pack(pady=10)

        for label, command in [
            ("🩺  Symptom-Based Prediction", self._launch_symptom),
            ("🧠  MRI Scan Classifier", self._launch_mri)
        ]:
            tk.Button(wrap, text=label, font=("Orbitron", 12, "bold"),
                      bg="#222", fg=FG_NEON, relief="flat",
                      activebackground="#333", activeforeground=FG_NEON,
                      command=command, padx=20, pady=15, width=30).pack(pady=5)

    def _build_collapsible_sections(self):
        self.sections = []
        for i, (heading, content) in enumerate(CONTENT_SECTIONS):
            section = CollapsibleSection(self.content_frame, heading, content, expanded=(i < 3))
            section.pack(fill="x", padx=10, pady=5)
            self.sections.append(section)

    def _run_search(self):
        query = self.search_var.get().strip().lower()
        if not query:
            return
        for section in self.sections:
            if query in section.title.lower() or query in section.content.lower():
                section.toggle_btn.config(bg="#005f5f")
                self.canvas.yview_moveto(section.winfo_y() / self.content_frame.winfo_height())
                self.root.after(1000, lambda btn=section.toggle_btn: btn.config(bg="#222"))
                break

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.root.configure(bg=BG_DARK if self.dark_mode else "#f7f7f7")

    def _show_sitemap(self):
        messagebox.showinfo("Sitemap", "\n".join(h for h, _ in CONTENT_SECTIONS))

    def _bind_keys(self):
        self.root.bind("/", lambda e: self.root.focus_get().tk_focusNext().focus())
        self.root.bind("<F11>", lambda e: self._toggle_fullscreen())

    def _toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def _launch_symptom(self):
        subprocess.Popen(["python3", "Symptom_predictor_ui.py"])
        self.root.destroy()  # ✅ Close dashboard after launching

    def _launch_mri(self):
        subprocess.Popen(["python3", "Xray_predictor_ui.py"])
        self.root.destroy()  # ✅ Close dashboard after launching



if __name__ == "__main__":
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()
