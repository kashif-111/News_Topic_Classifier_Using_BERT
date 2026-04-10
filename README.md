# News Topic Classifier Using BERT

## Objective
Fine-tune a pre-trained BERT (Bidirectional Encoder Representations from Transformers) model to classify news headlines into topic categories using the AG News Dataset.

## Methodology / Approach

### 1. **Dataset Loading & Preprocessing**
   - Load AG News dataset from Hugging Face Datasets
   - Explore data distribution across 4 classes (World, Sports, Business, Science/Tech)
   - Implement tokenization using BERT tokenizer

### 2. **Model Development & Training**
   - Use `bert-base-uncased` pre-trained model as base
   - Add classification head with dropout for regularization
   - Implement training loop with learning rate scheduling
   - Use AdamW optimizer with weight decay
   - Training configuration: 3 epochs, batch size 32, max sequence length 128

### 3. **Evaluation & Metrics**
   - **Accuracy**: Overall correctness of predictions
   - **F1-Score**: Macro average F1-score across all classes
   - Per-class precision, recall, and F1-score
   - Classification report and confusion matrix

### 4. **Deployment**
   - **Streamlit App** (`app_streamlit.py`): Interactive web interface
   - **Gradio App** (`app_gradio.py`): Alternative lightweight interface
   - Real-time prediction on user input headlines

## Key Results & Observations

The trained model will achieve:
- High accuracy on news classification (typically 90%+)
- Balanced F1-scores across all topic categories
- Fast inference time suitable for production deployment

## Project Structure

```
News_Classifier_using_BERT/
├── News_Classifier_BERT.ipynb          # Main Jupyter Notebook
├── app_streamlit.py                     # Streamlit deployment
├── app_gradio.py                        # Gradio deployment
├── models/                              # Saved model artifacts
│   └── bert_news_classifier/
├── data/                                # Dataset directory
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
```

## Installation & Setup

### 1. Clone/Create Project
```bash
cd c:\News_Classifier_using_BERT
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Jupyter Notebook
```bash
jupyter notebook News_Classifier_BERT.ipynb
```

### 4. Deploy with Streamlit
```bash
streamlit run app_streamlit.py
```

### 5. Deploy with Gradio
```bash
python app_gradio.py
```

## Dataset Information

**AG News Dataset:**
- **Size**: ~120,000 training + 7,600 test samples
- **Classes** (4 categories):
  - 1: World
  - 2: Sports
  - 3: Business
  - 4: Science/Technology
- **Features**: Text (headline) and Label

## Model Information

- **Base Model**: `bert-base-uncased`
- **Parameters**: ~109M
- **Max Sequence Length**: 128 tokens
- **Training Framework**: PyTorch with Hugging Face Transformers
- **GPU Memory**: ~4GB (GPU recommended)

## How to Use

### In Jupyter Notebook
- Run all cells sequentially
- Train the model
- Evaluate on test set
- Make predictions on custom sentences

### Streamlit App
```bash
streamlit run app_streamlit.py
```
- Enter any news headline
- Click "Classify" to see prediction and confidence scores

### Gradio App
```bash
python app_gradio.py
```
- Open browser to localhost URL
- Type headline and submit

## Technologies Used

- **Transformers**: Hugging Face Transformers library
- **Deep Learning**: PyTorch
- **NLP**: BERT, Tokenization
- **ML Pipeline**: scikit-learn
- **Visualization**: Matplotlib, Seaborn
- **Web Deployment**: Streamlit, Gradio
- **Data Handling**: Datasets, Pandas

## Performance Tips

1. **GPU Acceleration**: Use CUDA-compatible GPU for faster training
2. **Batch Optimization**: Adjust batch size based on available GPU memory
3. **Mixed Precision**: Enable mixed precision training for faster computation
4. **Gradient Accumulation**: Use to simulate larger batch sizes

## Future Improvements

- [ ] Implement cross-validation
- [ ] Hyperparameter tuning (learning rate, batch size, epochs)
- [ ] Test other BERT variants (DistilBERT, RoBERTa)
- [ ] Add confidence calibration
- [ ] Implement model explainability (LIME, SHAP)
- [ ] Create REST API with FastAPI

## Author
Kashif Ur Rahman
BS AI Student - AWKUM
DevelopersHub Corporation Internship

## License
MIT License
