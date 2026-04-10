# Advanced Usage and Improvements Guide

## 🚀 Advanced Features

### 1. Using DistilBERT (Faster Model)
Better for production deployment with less memory:

```python
# In your notebook, replace the model loading line:
model_name = 'distilbert-base-uncased'

# DistilBERT is 40% smaller and 60% faster than BERT
# with ~97% of BERT's performance
```

**Advantages:**
- 40% smaller model size
- 60% faster inference
- Lower memory requirements
- Better for mobile/edge deployment

**Trade-offs:**
- Slightly lower accuracy (~1-2%)

---

### 2. Model Quantization (Lightweight Deployment)

```python
from transformers import AutoModel
import torch

# Load and quantize model
model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=4)

# 8-bit quantization
model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)

# Reduces model size by ~4x with minimal accuracy loss
```

---

### 3. Ensemble Predictions

Combine multiple models for better accuracy:

```python
from transformers import AutoModelForSequenceClassification

models = [
    AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=4),
    AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=4),
    AutoModelForSequenceClassification.from_pretrained('roberta-base', num_labels=4)
]

def ensemble_predict(text, models):
    predictions = []
    for model in models:
        logits = model(**tokenizer(text, return_tensors='pt'))['logits']
        predictions.append(torch.softmax(logits, dim=1))
    
    # Average predictions
    ensemble_output = torch.mean(torch.stack(predictions), dim=0)
    return torch.argmax(ensemble_output, dim=1).item()
```

---

### 4. Model Explainability (SHAP)

Understand model predictions:

```bash
pip install shap[pytorch]
```

```python
import shap

# Create explainer
explainer = shap.Explainer(model, tokenizer)

# Explain prediction
headline = "Apple releases new iPhone with AI features"
shap_values = explainer([headline])

# Visualize
shap.plots.text(shap_values)
```

---

### 5. Fine-tuning on Custom Dataset

```python
from datasets import Dataset
import pandas as pd

# Load your custom data
df = pd.read_csv('your_data.csv')  # columns: 'text', 'label'

# Convert to HuggingFace Dataset
custom_dataset = Dataset.from_pandas(df)

# Follow the same training procedure from the notebook
# but with your custom data
```

---

### 6. Low-Rank Adaptation (LoRA)

Extremely efficient fine-tuning:

```bash
pip install peft
```

```python
from peft import LoraConfig, get_peft_model

# Create LoRA configuration
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["query", "value"],
    lora_dropout=0.1,
    bias="none",
    task_type="SEQ_CLS"
)

# Apply LoRA to model
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Now train as usual - only ~1% of parameters are trainable!
```

---

### 7. REST API Deployment with FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/predict")
async def predict(input_data: TextInput):
    pred_label, confidence, probs = classify_headline(
        input_data.text, model, tokenizer, device
    )
    
    return {
        "predicted_class": CLASS_LABELS[pred_label],
        "confidence": float(confidence),
        "probabilities": {
            CLASS_LABELS[i]: float(probs[i]) 
            for i in range(4)
        }
    }

# Run: uvicorn app:app --reload
```

---

### 8. Caching for Faster Inference

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_predict(headline_hash):
    # This won't work directly because headlines aren't hashable
    # Instead, use joblib:
    pass

from joblib import Memory
memory = Memory(location='cache_dir', verbose=0)

@memory.cache
def cached_predict(headline):
    return classify_headline(headline, model, tokenizer, device)

# Results are cached and reused automatically
```

---

### 9. Hyperparameter Tuning with Ray Tune

```bash
pip install ray[tune]
```

```python
from ray import tune
from ray.air import session

def train_model(config):
    # config contains different hyperparameters to test
    LEARNING_RATE = config['lr']
    BATCH_SIZE = config['batch_size']
    # ... train model ...
    session.report({"accuracy": accuracy})

best_result = tune.run(
    train_model,
    config={
        "lr": tune.loguniform(1e-5, 1e-3),
        "batch_size": tune.choice([16, 32, 64])
    },
    num_samples=10,
    metric="accuracy",
    mode="max"
)
```

---

### 10. Model Serving with TensorFlow Serving

Convert model to ONNX and deploy:

```bash
pip install optimum onnx onnxruntime
```

```python
from optimum.onnxruntime import ORTModelForSequenceClassification

# Export to ONNX
ort_model = ORTModelForSequenceClassification.from_pretrained(
    'models/bert_news_classifier',
    from_transformers=True
)

# Save
ort_model.save_pretrained('onnx_model')

# Inference is now ~2-3x faster
from optimum.onnxruntime import ORTModelForSequenceClassification
# Use for inference
```

---

## 📊 Performance Optimization Checklist

- [ ] Profile code with `cProfile` for bottlenecks
- [ ] Use mixed precision training (fp16) for 2x speedup
- [ ] Implement batch inference (process multiple samples together)
- [ ] Cache model outputs for repeated predictions
- [ ] Use quantization for smaller model size
- [ ] Profile GPU memory usage
- [ ] Implement model distillation for smaller model

---

## 🔍 Evaluation Beyond Accuracy

```python
# Cross-validation for better evaluation
from sklearn.model_selection import cross_val_score, cross_validate

scorer = {
    'accuracy': 'accuracy',
    'precision_macro': 'precision_macro',
    'recall_macro': 'recall_macro',
    'f1_macro': 'f1_macro'
}

cv_results = cross_validate(
    model, X, y, cv=5, scoring=scorer
)

print(f"Mean Accuracy: {cv_results['test_accuracy'].mean():.4f}")
print(f"Mean F1: {cv_results['test_f1_macro'].mean():.4f}")
```

---

## 🌍 Multilingual Support

```python
# Use multilingual BERT for multiple languages
model_name = 'bert-base-multilingual-uncased'

# Supports: Arabic, Chinese, English, French, German, Hindi, 
#           Japanese, Korean, Spanish, Portuguese, Italian, Russian, etc.

# Training process is identical!
```

---

## 📚 Additional Resources

### Papers to Read
1. BERT: https://arxiv.org/abs/1810.04805 (2018)
2. DistilBERT: https://arxiv.org/abs/1910.01108 (2019)
3. RoBERTa: https://arxiv.org/abs/1907.11692 (2019)
4. ALBERT: https://arxiv.org/abs/1909.11942 (2019)

### Useful Courses
- Hugging Face NLP Course: https://huggingface.co/course
- Stanford CS224N: https://web.stanford.edu/class/cs224n/

### Tools & Libraries
- PyTorch: https://pytorch.org/
- Transformers: https://huggingface.co/transformers/
- W&B for experiment tracking: https://wandb.ai/
- Optuna for hyperparameter tuning: https://optuna.org/

---

## 🎯 Next Steps for Your Portfolio

1. ✅ Complete Task 1 (This BERT classifier)
2. 📝 Complete 2 more tasks from the list
3. 🏆 Implement one advanced feature (quantization, distillation, etc.)
4. 📊 Create comparison graphs of different approaches
5. 🚀 Deploy a live demo
6. 💼 Share on GitHub and LinkedIn
7. 📖 Write a blog post about your approach

---

**Keep learning and experimenting! 🚀**
