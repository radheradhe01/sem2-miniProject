# Fashion Product Analysis and Search Engine

This project implements a system for analyzing fashion product images using OpenAI's CLIP model, storing the extracted information, and providing search capabilities. It includes components for database creation, a Streamlit demo for image-to-description, a core backend application, and potentially a Flutter frontend.

## Overview

The system aims to:
1.  **Analyze Images:** Use CLIP to extract attributes like category, color, brand, and gender from fashion product images.
2.  **Store Data:** Create and populate a database (likely vector-based) with image features and metadata.
3.  **Search:** Allow users to search for products based on text descriptions or potentially image similarity.
4.  **Demonstrate:** Provide a simple Streamlit interface (`demos/clipTest.py`) to showcase the CLIP image-to-text capability.

## Features

*   **CLIP-based Image Analysis:** Extracts semantic features and attributes from product images.
*   **Database Creation:** Scripts and notebooks to process datasets and build the search database.
*   **Text-to-Image Search:** Core search functionality implemented in `search.py` and `main.py`.
*   **Streamlit Demo:** An interactive demo (`demos/clipTest.py`) for uploading an image and getting a generated description.
*   **Docker Support:** `Dockerfile` and `docker-compose.yml` for containerized deployment.
*   **(Potential) Flutter Frontend:** A `frontend/flutter` directory suggests a mobile or web application interface is planned or in development.

## Project Structure

```
.
├── createDatabase.py         # Script to create/populate the main database
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration for the application
├── main.py                   # Main backend application entry point (likely API/search server)
├── prompt_templates.py       # Templates for generating text descriptions or prompts
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── search.py                 # Core search logic implementation
├── Test.ipynb                # Jupyter notebook for testing/experiments
├── database_creators/        # Scripts/notebooks for dataset processing and DB creation
│   ├── Amazon Database Creater.ipynb
│   ├── CleanedProducts Database creator.ipynb
│   └── datasets_csv/         # Raw CSV datasets
├── demos/                    # Demonstration applications
│   ├── clip_demo.py          # Another CLIP demo (potentially different focus)
│   └── clipTest.py           # Streamlit demo for image-to-description
├── frontend/                 # Frontend application code
│   └── flutter/              # Flutter application source
├── images/                   # Sample or test images
└── __pycache__/              # Python cache files (usually ignored)
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure you have a compatible Python version, e.g., Python 3.8+)*

3.  **(Optional) Docker Setup:** If using Docker:
    ```bash
    docker-compose up --build
    ```
    *(This will build the image defined in `Dockerfile` and start services defined in `docker-compose.yml`)*

## Usage

### 1. Database Creation

*   Run the database creation scripts/notebooks in `database_creators/` to process your datasets (e.g., those in `datasets_csv/`).
*   Execute `createDatabase.py` to populate the search database (the exact command might depend on its implementation, e.g., `python createDatabase.py`).

### 2. Running the Main Application (Search Backend)

*   Start the main application, which likely serves the search API:
    ```bash
    uvicorn main:app --port 9999 --reload
    ```
    *(Or use the Docker command if running containerized)*

### 3. Running the Streamlit Demo

*   Navigate to the demos directory and run the Streamlit app:
    ```bash
    streamlit run demos/clipTest.py
    ```
*   Open the URL provided by Streamlit (usually `http://localhost:8501`) in your browser.
*   Upload an image to see the generated description.

### 4. (Potential) Running the Flutter Frontend

*   Navigate to `frontend/flutter/`.
*   Follow standard Flutter procedures to build and run the app (e.g., `flutter run`). Requires Flutter SDK setup.

## Technologies Used

*   **Python:** Core backend language.
*   **OpenAI CLIP:** For image embedding and analysis.
*   **PyTorch:** Deep learning framework (used by CLIP).
*   **Streamlit:** For creating the interactive web demo.
*   **Pandas/NumPy:** (Likely used in database creation/data handling).
*   **Docker:** For containerization.
*   **Flutter/Dart:** (Potential) For the frontend application.
*   **(Potential) Vector Database:** Such as FAISS, Milvus, Pinecone, ChromaDB (depending on `createDatabase.py` and `search.py` implementation).

## Acknowledgements

*   [OpenAI CLIP](https://github.com/openai/CLIP)
*   [Streamlit](https://streamlit.io/)
*   *(Add any other libraries, datasets, or inspirations)*

