# News_Topic_Classifier_Using_BERT
A news topic classification project using BERT for accurate text categorization. Leverages pretrained transformer models to understand contextual meaning in news articles. Supports multiple categories such as politics,sports, business, technology. Includes data preprocessing, model fine-tuning,. Built with Python, Pytorch, and Hugging Face scalable NLP workflows.
📰 News Topic Classifier using BERT
📌 Overview

This project implements a news topic classification system using BERT (Bidirectional Encoder Representations from Transformers). The model is fine-tuned on a labeled news dataset to accurately classify articles into predefined categories such as politics, sports, business, and technology.

🚀 Features
Uses pretrained BERT for deep contextual understanding
Fine-tuned on custom/news datasets
Supports multi-class classification
End-to-end pipeline (preprocessing → training → evaluation)
High accuracy with minimal feature engineering
🛠️ Tech Stack
Python
PyTorch
Hugging Face Transformers
Scikit-learn
Pandas & NumPy
📂 Project Structure
├── data/               # Dataset files
├── notebooks/          # Jupyter notebooks (EDA, experiments)
├── src/                # Source code
│   ├── preprocessing.py
│   ├── train.py
│   ├── evaluate.py
├── models/             # Saved models
├── requirements.txt
└── README.md
⚙️ Installation
git clone https://github.com/your-username/news-topic-classifier-bert.git
cd news-topic-classifier-bert
pip install -r requirements.txt
▶️ Usage
python src/train.py
python src/evaluate.py
📊 Model Details
Model: bert-base-uncased
Task: Multi-class text classification
Metrics: Accuracy, Precision, Recall, F1-score
📈 Results

The model achieves strong performance due to BERT’s ability to capture contextual relationships in text.

🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

📜 License

This project is licensed under the MIT License.
