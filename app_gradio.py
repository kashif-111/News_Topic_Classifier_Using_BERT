# ============================================================================
# GRADIO WEB APPLICATION FOR NEWS CLASSIFIER
# ============================================================================
# Run with: python app_gradio.py

import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

# ============================================================================
# MODEL LOADING
# ============================================================================

# Check if model exists
model_path = 'models/bert_news_classifier'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"""
    Model not found at {model_path}
    Please run the training notebook first: News_Classifier_BERT.ipynb
    """)

# Load model and tokenizer
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
model.eval()

print(f"Model loaded successfully!")
print(f"Device: {device}")

# Class labels
CLASS_LABELS = {
    0: 'World 🌍',
    1: 'Sports ⚽',
    2: 'Business 💼',
    3: 'Science/Technology 🔬'
}

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================

def classify_headline(headline: str) -> str:
    """
    Classify a news headline using the fine-tuned BERT model.
    
    Args:
        headline: Input news headline text
        
    Returns:
        Formatted prediction results
    """
    
    if not headline or headline.strip() == "":
        return "⚠️ Please enter a headline!"
    
    try:
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
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            
            # Get probabilities
            probabilities = torch.softmax(logits, dim=1)[0]
            pred_label = torch.argmax(logits, dim=1).item()
            confidence = probabilities[pred_label].item()
        
        # Format output
        result = f"""
        <div style='text-align: center; background-color: #f0f0f0; padding: 20px; border-radius: 10px;'>
            <h2 style='color: #1f77b4;'>Predicted Category: <strong>{CLASS_LABELS[pred_label]}</strong></h2>
            <h3 style='color: #666;'>Confidence Score: <strong>{confidence:.2%}</strong></h3>
            
            <hr style='margin: 20px 0;'>
            
            <h3>All Category Predictions:</h3>
            <table style='margin: auto; border-collapse: collapse; width: 100%;'>
                <tr style='background-color: #e0e0e0;'>
                    <th style='border: 1px solid #ccc; padding: 10px;'>Category</th>
                    <th style='border: 1px solid #ccc; padding: 10px;'>Confidence</th>
                    <th style='border: 1px solid #ccc; padding: 10px;'>Percentage</th>
                </tr>
        """
        
        # Add rows for each class
        # Sort by probability in descending order to show ranking
        sorted_probs = sorted(enumerate(probabilities.cpu().numpy()), 
                             key=lambda x: x[1], reverse=True)
        
        for idx, prob in sorted_probs:
            result += f"""
                <tr>
                    <td style='border: 1px solid #ccc; padding: 10px; text-align: left;'>{CLASS_LABELS[idx]}</td>
                    <td style='border: 1px solid #ccc; padding: 10px;'>{prob:.4f}</td>
                    <td style='border: 1px solid #ccc; padding: 10px;'>{prob*100:.2f}%</td>
                </tr>
            """
        
        result += """
            </table>
        </div>
        """
        
        return result
    
    except Exception as e:
        return f"❌ Error during classification: {str(e)}"

# ============================================================================
# GRADIO INTERFACE
# ============================================================================

# Define input and output components
input_textbox = gr.Textbox(
    label="News Headline",
    placeholder="Enter a news headline here...",
    lines=3,
    max_lines=5,
)

output_html = gr.HTML(label="Prediction Results")

# Example headlines
examples = [
    ["Apple releases iPhone 15 with advanced AI capabilities"],
    ["Manchester United advances to Champions League final"],
    ["Federal Reserve raises interest rates to combat inflation"],
    ["Scientists discover new pathway for treating Alzheimer's disease"],
    ["China launches new space station in Earth orbit"],
    ["Tech company announces layoffs affecting 10,000 employees"]
]

# Create interface
interface = gr.Interface(
    fn=classify_headline,
    inputs=input_textbox,
    outputs=output_html,
    title="📰 News Topic Classifier - BERT Fine-Tuned Model",
    description="""
    <div style='text-align: center; font-size: 1.1rem; margin-bottom: 20px;'>
        This application classifies news headlines into 4 categories using a fine-tuned BERT model trained on the AG News dataset.
        <br><br>
        <strong>Categories:</strong> World 🌍 | Sports ⚽ | Business 💼 | Science/Technology 🔬
    </div>
    """,
    examples=examples,
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
    ),
    flagging_options=["Correct Prediction", "Incorrect Prediction", "Needs Review"]
)

# Add custom CSS styling
interface.css = """
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .gradio-container { max-width: 900px; margin: auto; }
    .gradio-interface { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    h1 { color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
"""

# ============================================================================
# LAUNCH APPLICATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 LAUNCHING GRADIO APPLICATION")
    print("="*80)
    print("\nNote: Check console output for the URL to access the application.")
    print("Usually available at: http://localhost:7860/")
    print("\nPress Ctrl+C to stop the server.")
    print("="*80 + "\n")
    
    # Launch the interface
    interface.launch(
        share=False,  # Set to True to get a public link (temporary)
        server_name="0.0.0.0",  # Listen on all network interfaces
        server_port=7860,  # Port number
    )
