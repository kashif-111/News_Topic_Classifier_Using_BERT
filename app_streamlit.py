# ============================================================================
# STREAMLIT WEB APPLICATION FOR NEWS CLASSIFIER
# ============================================================================
# Run with: streamlit run app_streamlit.py

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from datetime import datetime
import os

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="News Topic Classifier",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .header {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subheader {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .prediction-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.subheader("Model Information")
    st.info("""
    - **Model**: BERT (bert-base-uncased)
    - **Task**: News Topic Classification
    - **Categories**: 4 classes
    - **Max Input Length**: 128 tokens
    """)
    
    st.subheader("About This App")
    st.markdown("""
    This application classifies news headlines into four categories:
    1. **World** 🌍
    2. **Sports** ⚽
    3. **Business** 💼
    4. **Science/Technology** 🔬
    
    It uses a fine-tuned BERT model trained on the AG News dataset.
    """)
    
    st.divider()
    st.markdown("**Author**: Kashif Ur Rahman | AWKUM | DevelopersHub Corp")
    st.markdown("**Internship**: AI/ML Engineering Advanced Tasks")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

# Load model and tokenizer with caching
@st.cache_resource
def load_model_and_tokenizer():
    """Load the fine-tuned BERT model and tokenizer."""
    model_path = 'models/bert_news_classifier'
    
    # Check if model exists
    if not os.path.exists(model_path):
        st.error(f"""
        ❌ Model not found at `{model_path}`
        
        Please ensure you have:
        1. Run the training notebook: `News_Classifier_BERT.ipynb`
        2. Model files are saved in `models/bert_news_classifier/`
        """)
        st.stop()
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    
    # Move to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    return model, tokenizer, device

# Load model
model, tokenizer, device = load_model_and_tokenizer()

# Class labels
class_labels = {
    0: ('World', '🌍'),
    1: ('Sports', '⚽'),
    2: ('Business', '💼'),
    3: ('Science/Technology', '🔬')
}

# Title and description
st.markdown('<div class="header">📰 News Topic Classifier</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subheader">Powered by Fine-tuned BERT | Real-time News Classification</div>',
    unsafe_allow_html=True
)

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================

def classify_headline(headline, model, tokenizer, device):
    """Classify a news headline and return predictions."""
    model.eval()
    
    with torch.no_grad():
        # Tokenize input
        encodings = tokenizer(
            headline,
            max_length=128,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        
        # Move to device
        input_ids = encodings['input_ids'].to(device)
        attention_mask = encodings['attention_mask'].to(device)
        
        # Get predictions
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        
        # Get probabilities
        probabilities = torch.softmax(logits, dim=1)[0]
        pred_label = torch.argmax(logits, dim=1).item()
        confidence = probabilities[pred_label].item()
        
    return pred_label, confidence, probabilities.cpu().numpy()

# ============================================================================
# USER INPUT AND CLASSIFICATION
# ============================================================================

# Create tabs for different interaction modes
tab1, tab2, tab3 = st.tabs(["🔍 Classify Headline", "📊 Batch Predictions", "ℹ️ Help"])

with tab1:
    st.subheader("Enter a News Headline")
    
    # Input options
    input_method = st.radio(
        "Choose input method:",
        ["Type Headline", "Use Preset Examples"],
        horizontal=True
    )
    
    if input_method == "Type Headline":
        headline = st.text_area(
            "Enter your news headline:",
            height=100,
            placeholder="e.g., Apple releases new iPhone 15 with advanced AI features..."
        )
    else:
        examples = {
            "World News": "United Nations calls for emergency meeting on climate crisis",
            "Sports": "Manchester United wins Champions League final after penalty shootout",
            "Business": "Tesla stock surges after announcing record quarterly profits",
            "Science": "Scientists discover new species of deep-sea fish in Mariana Trench"
        }
        selected_example = st.selectbox("Choose an example:", list(examples.keys()))
        headline = examples[selected_example]
    
    # Add a button to classify
    col1, col2 = st.columns([3, 1])
    
    with col1:
        classify_button = st.button("🚀 Classify Headline", use_container_width=True)
    
    if classify_button and headline:
        # Show loading state
        with st.spinner("Analyzing headline..."):
            pred_label, confidence, probabilities = classify_headline(
                headline, model, tokenizer, device
            )
        
        # Display prediction
        st.success("✅ Classification Complete!")
        
        # Main prediction box
        class_name, emoji = class_labels[pred_label]
        st.markdown(
            f"""
            <div class="prediction-box">
                <h2>{emoji} Predicted Class: <strong>{class_name}</strong></h2>
                <h3>Confidence: <strong>{confidence:.2%}</strong></h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Confidence scores for all classes
        st.subheader("📊 Confidence Scores for All Categories")
        
        # Create columns for metrics
        cols = st.columns(4)
        for i, (label, emoji) in class_labels.items():
            with cols[i]:
                st.metric(
                    f"{emoji} {label}",
                    f"{probabilities[i]:.2%}",
                    delta=None
                )
        
        # Detailed breakdown
        st.subheader("📈 Detailed Breakdown")
        prob_df = {
            'Category': [class_labels[i][0] for i in range(4)],
            'Emoji': [class_labels[i][1] for i in range(4)],
            'Confidence': [f"{probabilities[i]:.4f}" for i in range(4)],
            'Percentage': [f"{probabilities[i]:.2%}" for i in range(4)]
        }
        
        # Bar chart
        import pandas as pd
        df = pd.DataFrame(prob_df)
        
        st.bar_chart(
            data={
                'Category': [class_labels[i][0] for i in range(4)],
                'Probability': probabilities
            },
            x='Category',
            y='Probability'
        )
        
        # Show the input headline
        st.subheader("📝 Input Headline")
        st.write(f"_{headline}_")
        
    elif classify_button and not headline:
        st.warning("⚠️ Please enter a headline to classify!")

with tab2:
    st.subheader("Batch Predictions")
    
    batch_text = st.text_area(
        "Enter multiple headlines (one per line):",
        height=200,
        placeholder="Headline 1\nHeadline 2\nHeadline 3\n..."
    )
    
    if st.button("🚀 Classify All Headlines", use_container_width=True):
        if batch_text:
            headlines = [h.strip() for h in batch_text.split('\n') if h.strip()]
            
            if headlines:
                st.info(f"Classifying {len(headlines)} headlines...")
                
                results = []
                progress_bar = st.progress(0)
                
                for idx, headline in enumerate(headlines):
                    with st.spinner(f"Processing headline {idx+1}/{len(headlines)}"):
                        pred_label, confidence, probs = classify_headline(
                            headline, model, tokenizer, device
                        )
                        
                        class_name, emoji = class_labels[pred_label]
                        results.append({
                            'Headline': headline,
                            'Category': class_name,
                            'Emoji': emoji,
                            'Confidence': f"{confidence:.2%}"
                        })
                    
                    progress_bar.progress((idx + 1) / len(headlines))
                
                # Display results
                st.success("✅ All headlines classified!")
                
                import pandas as pd
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)
                
                # Download results
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv,
                    file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("⚠️ Please enter at least one headline!")

with tab3:
    st.subheader("How to Use")
    
    st.markdown("""
    ### 📍 Steps to Classify News Headlines:
    
    1. **Go to "Classify Headline" Tab** 👈
    2. **Enter or Select a News Headline**
       - Type your own headline, or
       - Choose from preset examples
    3. **Click "Classify Headline" Button**
    4. **View Results**
       - Main prediction with confidence score
       - Confidence scores for all categories
       - Visual breakdown of probabilities
    
    ### 📊 Understanding the Results:
    
    - **Predicted Class**: The most likely news category
    - **Confidence**: How confident the model is (higher is better)
    - **Category Scores**: Probability distribution across all categories
    
    ### 🏷️ News Categories:
    
    - **🌍 World**: International news, global events, politics
    - **⚽ Sports**: Sports news, games, athletes, competitions
    - **💼 Business**: Business news, markets, finance, companies
    - **🔬 Science/Technology**: Technology, science discoveries, innovation
    
    ### 💡 Tips for Better Results:
    
    - Use clear, concise headlines
    - Keep headlines under 128 tokens (~25 words)
    - Avoid overly ambiguous headlines
    - Include relevant keywords for the topic
    
    ### 📚 Model Information:
    
    - **Base Model**: BERT (Bidirectional Encoder Representations from Transformers)
    - **Training Data**: AG News Dataset
    - **Architecture**: Fine-tuned for sequence classification
    - **Input Size**: 128 tokens (max)
    - **Output**: 4-class classification
    
    ### ⚙️ System Information:
    
    - **Device**: {device}
    - **Model Path**: `models/bert_news_classifier/`
    - **Tokenizer**: BERT Tokenizer
    """.replace('{device}', str(device)))

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;'>
    <p>🎓 AI/ML Engineering Internship | DevelopersHub Corporation</p>
    <p>Built with ❤️ by Kashif Ur Rahman | AWKUM | March 2026</p>
</div>
""", unsafe_allow_html=True)
