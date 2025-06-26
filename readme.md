# Sentiment Analysis Web App - Setup Instructions

## 📁 Project Structure
Create this folder structure on your computer:

```
sentiment_analyzer/
├── app.py
├── model_trainer.py
├── requirements.txt
├── data/
│   └── training.1600000.processed.noemoticon.csv
├── models/
│   └── (models will be saved here)
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── index.html
    └── result.html
```

## 🚀 Step-by-Step Setup

### 1. Create Project Directory
```bash
mkdir sentiment_analyzer
cd sentiment_analyzer
```

### 2. Create Required Folders
```bash
mkdir data models static templates
```

### 3. Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 4. Download Dataset
- Download the Sentiment140 dataset: `training.1600000.processed.noemoticon.csv`
- Place it in the `data/` folder
- **Dataset Link**: [Sentiment140 Dataset from Kaggle](https://www.kaggle.com/datasets/kazanova/sentiment140)

### 5. Train the Model
```bash
python model_trainer.py
```
This will:
- Load and preprocess the dataset
- Train the RNN model
- Save model to `models/sentiment_model.h5`
- Save tokenizer to `models/tokenizer.pkl`

### 6. Run the Web Application
```bash
python app.py
```

### 7. Access the Application
Open your browser and go to: `http://localhost:5000`

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask web application |
| `model_trainer.py` | Script to train and save the ML model |
| `templates/index.html` | Home page with input form |
| `templates/result.html` | Results page showing sentiment |
| `static/style.css` | Custom CSS styling |
| `static/script.js` | Frontend JavaScript functionality |
| `requirements.txt` | Python dependencies |

## 🎯 How to Use

1. **Enter text** in the textarea on the home page
2. **Click "Analyze Sentiment"** button
3. **View results** showing:
   - Sentiment (Positive 😊 / Negative 😞 / Neutral 😐)
   - Confidence percentage
   - Visual progress bar

## 🛠 Features

- **Clean web interface** with Bootstrap styling
- **Real-time sentiment analysis** using trained RNN model
- **Example texts** to try quickly
- **Character counter** and input validation
- **Responsive design** for mobile devices
- **API endpoint** at `/api/predict` for programmatic access

## 🧠 Model Details

- **Architecture**: Simple RNN with Embedding layer
- **Training Data**: 1.6M tweets from Sentiment140 dataset
- **Preprocessing**: Text cleaning, tokenization, padding
- **Output**: Binary classification (0=Negative, 1=Positive)

## 🚨 Troubleshooting

### Model Not Found Error
```bash
# Run the trainer first
python model_trainer.py
```

### Dataset Not Found
- Ensure `training.1600000.processed.noemoticon.csv` is in `data/` folder
- Download from Kaggle Sentiment140 dataset

### Port Already in Use
```bash
# Kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

### Dependencies Issues
```bash
# Upgrade pip first
pip install --upgrade pip

# Install specific versions
pip install tensorflow==2.13.0
```

## 📊 API Usage

Send POST request to `/api/predict`:
```javascript
fetch('/api/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: 'I love this product!'})
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🎉 You're Ready!
Your sentiment analysis web app is now running locally at `http://localhost:5000`