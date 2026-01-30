# 🌶️ AI Crop - Chili Disease Detection

AI Crop is a modern web application powered by **Flask** and **YOLOv8** to detect diseases in chili plants. It features a stylish, glassmorphism-inspired UI and processes images securely in-memory without saving user data to the server.

## 🚀 Features

*   **Real-time Disease Detection**: Uses a custom trained YOLOv8 model (`best.pt`) to identify chili plant diseases (e.g., Cercospora, Bacterial Spot, Curl Virus).
*   **Privacy-Focused**: Images are processed in-memory and never saved to the disk.
*   **Modern UI**: Responsive design with Glassmorphism effects, smooth animations, and a fresh emerald green theme.
*   **External Integration**: Automatically sends diagnosis results to a **Botpress** webhook.
*   **Confidence Scoring**: Displays detailed confidence percentages for each diagnosis.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **AI/ML**: Ultralytics YOLOv8, Pillow (PIL)
*   **Frontend**: HTML5, CSS3 (Modern Variables, Flexbox/Grid), Vanilla JavaScript

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/bapakKau00/agrichat_chili.git
    ```

2.  **Create a virtual environment** (Optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Place your model**:
    Ensure your trained YOLOv8 model file (`best.pt`) is in the root directory.

## 🏃 Usage

1.  **Run the application**:
    ```bash
    python app.py
    ```

3.  **Detect Diseases**:
    *   Drag and drop a chili leaf image or click to upload.
    *   The AI will analyze the image and display the diagnosis immediately.
    *   Results are automatically sent to the configured webhook.

## 🔧 Configuration

*   **Webhook**: Passed the model inference to botpress using webhook.

## 📄 License

This project is open-source and available for educational and agricultural use.
