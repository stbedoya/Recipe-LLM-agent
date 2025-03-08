# Recipe Generator

The **Recipe Generator** is a FastAPI-based application that generates recipes using OpenAI's API and validates them against predefined ingredient constraints. The application stores and retrieves data using MongoDB.

## How It Works

1. **Clone the Repository**: You’ll need to download the project files to your local machine.
2. **Set up MongoDB**: The application requires MongoDB running locally to store and retrieve recipes.
3. **Configure the Application**: Adjust configurations in the `config.py` file, such as OPEN AI API key.
4. **Run the Application**: Start the FastAPI app using Uvicorn and access the API via `http://localhost:8000`.

## 🚀 Getting Started

Follow these steps to set up and run the Recipe Generator locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/stbedoya/recipe_agent.git
cd recipe_agent
```

### 2️⃣ Start MongoDB (Linux)

Ensure that you have MongoDB installed and running. You can start MongoDB with:

```bash
sudo systemctl start mongod
```

### 3️⃣ Configure OpenAI API Key

Update your config file (e.g., `config.py` or `.env`) with your OpenAI API key:

```python
OPENAI_API_KEY = "your-openai-api-key"
```

Or, if using an `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
```

### 4️⃣ Install Dependencies

Ensure you have Python 3.11+ installed, then install dependencies:

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
pip install -r requirements.txt
```

### 5️⃣ Run the API

Start the FastAPI application using Uvicorn:

```bash
uvicorn src.api.routers:app --reload
```

### 6️⃣ Test the API

Once running, access the interactive documentation at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
