# News Topic Classifier - Quick Start Guide

## ⚡ Quick Installation and Running

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Train the Model (Using Jupyter Notebook)
```bash
jupyter notebook News_Classifier_BERT.ipynb
```
- Run all cells sequentially
- This will train the model and save it to `models/bert_news_classifier/`
- Training takes approximately 10-15 minutes on GPU (CPU: 30-45 minutes)

### Step 3: Deploy with Streamlit
```bash
streamlit run app_streamlit.py
```
- Open browser to: http://localhost:8501
- Features:
  - Type or paste news headlines
  - Get instant classifications
  - View confidence scores
  - Batch predict multiple headlines
  - Download predictions as CSV

### Step 4: Deploy with Gradio
```bash
python app_gradio.py
```
- Open browser to: http://localhost:7860
- Lightweight, interactive interface
- Supports flagging predictions for review

---

## 📁 Project Structure

```
News_Classifier_using_BERT/
│
├── News_Classifier_BERT.ipynb       # Main training notebook
├── app_streamlit.py                  # Streamlit web app
├── app_gradio.py                     # Gradio web app
├── requirements.txt                  # Python dependencies
├── README.md                         # Full documentation
├── QUICKSTART.md                     # This file
│
├── models/                           # Saved models
│   └── bert_news_classifier/
│       ├── config.json
│       ├── pytorch_model.bin
│       ├── tokenizer.json
│       ├── vocab.txt
│       └── special_tokens_map.json
│
└── *.png                            # Generated visualizations
    ├── class_distribution.png
    ├── training_history.png
    └── confusion_matrix.png
```

---

## 💻 Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB |
| VRAM (GPU) | 2 GB | 4+ GB |
| Storage | 2 GB | 5 GB |
| CPU | i5/Ryzen 5 | i7/Ryzen 7 |

### Without GPU (CPU Only)
- Training: ~30-45 minutes
- Inference: ~0.5-1 second per headline

### With GPU (CUDA)
- Training: ~10-15 minutes
- Inference: ~0.05-0.1 second per headline

---

## 🎯 Using the Applications

### Streamlit App Features
- ✅ Single headline classification
- ✅ Batch predictions (multiple headlines)
- ✅ Confidence visualization
- ✅ CSV export
- ✅ Interactive examples
- ✅ Real-time processing

### Gradio App Features
- ✅ Simple web interface
- ✅ Example headlines provided
- ✅ Lightweight deployment
- ✅ Flagging system for review
- ✅ Mobile-friendly

---

## 📊 Expected Performance

After training on the AG News dataset:
- **Overall Accuracy**: ~90-92%
- **F1-Score (Macro)**: ~0.89-0.91
- **Per-class F1**: ~0.88-0.92 across all categories

---

## 🐛 Troubleshooting

### Issue: "Model not found"
```
Solution: Run the Jupyter notebook first to train and save the model
```

### Issue: "Out of Memory"
```
Solutions:
1. Reduce batch size in notebook (line with BATCH_SIZE = 32)
2. Use CPU only (set device = torch.device('cpu'))
3. Use a lighter model (DistilBERT instead of BERT)
```

### Issue: "GPU not detected"
```
Solution: Install CUDA and PyTorch with GPU support:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Issue: "Tokenizer download fails"
```
Solution: Download model manually:
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('bert-base-uncased')"
```

---

## 🔗 Useful Links

- **Hugging Face Hub**: https://huggingface.co/
- **AG News Dataset**: https://huggingface.co/datasets/ag_news
- **BERT Paper**: https://arxiv.org/abs/1810.04805
- **Transformers Library**: https://huggingface.co/docs/transformers
- **Streamlit Docs**: https://docs.streamlit.io/
- **Gradio Docs**: https://www.gradio.app/docs/

---

## 📝 Submission Checklist

- [ ] Jupyter Notebook with all sections completed
- [ ] Model trained and saved
- [ ] README.md with documentation
- [ ] Streamlit app working
- [ ] Gradio app working (optional)
- [ ] Visualizations generated (plots saved)
- [ ] Code well-commented and structured
- [ ] GitHub repository created
- [ ] GitHub link submitted to Google Classroom

---

## 🎓 Learning Outcomes

After completing this task, you should understand:
- ✅ Transfer learning with transformers
- ✅ Fine-tuning pre-trained models
- ✅ NLP preprocessing and tokenization
- ✅ Model evaluation metrics
- ✅ Web application deployment
- ✅ PyTorch and Hugging Face Transformers
- ✅ Production-ready ML pipelines

---

**Good luck with your internship! 🚀**
