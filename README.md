# Recipe LLM agent Service

A toy backend service that exposes a REST API for managing ingredient preferences and generating personalized recipes using a Large Language Model (LLM). Built to demonstrate production-quality Python backend skills and the ability to effectively leverage LLMs for data synthesis and transformation.

## 🚀 Features

### 1. Ingredient Preferences Management

- **CRUD API** to manage user ingredient preferences.
- **Preferences** indicate whether an ingredient is liked or disliked.
- **Persistence**: All preferences are stored in a **MongoDB** database.
- **Validation**:
  - Input is validated using **Pydantic** models.
  - Contradictory preferences (e.g., liking and disliking the same ingredient) are not allowed.

### 2. Recipe Generation

A core endpoint for generating personalized recipes:

- Accepts a list of **available ingredients**.
- Leverages stored user preferences and an **LLM** to generate appropriate recipes.
- Filters out recipes that contain **disliked ingredients**.
- Returns up to **5 structured recipes** in JSON format, each including:
  - Recipe name
  - Ingredients list (with quantities)
  - Step-by-step cooking instructions
  - Estimated cooking time
  - Difficulty level

### 3. Quality Assurance

- **LLM Response Validation**:
  - Ensures response follows the expected structure.
  - Checks that no disliked ingredients appear in recipes.
  - Verifies recipe completeness and culinary coherence.
- Handles **edge cases** like:
  - Conflicting preferences
  - Insufficient ingredients

##  Tech Stack

- **Python** (FastAPI for the REST API)
- **Pydantic** for request/response validation
- **MongoDB** for data persistence 
- **LLM** integration via OpenAI API
  
## How It Works

1. **Clone the Repository**: You’ll need to download the project files to your local machine.
2. **Set up MongoDB**: The application requires MongoDB running locally to store and retrieve recipes.
3. **Configure the Application**: Adjust configurations in the `config.py` file, such as OPEN AI API key.
4. **Run the Application**: Start the FastAPI app using Uvicorn and access the API via `http://localhost:8000`.

## Getting Started

Follow these steps to set up and run the Recipe Generator locally.

### Clone the Repository

```bash
git clone https://github.com/stbedoya/recipe_agent.git
cd recipe_agent
```

### Start MongoDB (Linux)

Ensure that you have MongoDB installed and running. You can start MongoDB with:

```bash
sudo systemctl start mongod
```

### Configure OpenAI API Key

Update your config file (e.g., `config.py` or `.env`) with your OpenAI API key:

```python
OPENAI_API_KEY = "your-openai-api-key"
```

Or, if using an `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
```

### Install Dependencies

Ensure you have Python 3.11+ installed, then install dependencies:

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
pip install -r requirements.txt
```

### Run the API

Start the FastAPI application using Uvicorn:

```bash
uvicorn src.api.routers:app --reload
```

### Test the API

Once running, access the interactive documentation at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
