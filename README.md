# Car Price Predictor: Enterprise-Grade Machine Learning Architecture

## Executive Summary
The Car Price Predictor is a full-stack, microservices-driven web application engineered to predict the market value of used vehicles with high accuracy. Utilizing historical data encompassing manufacturer, model, production year, and mileage, the application leverages machine learning models to generate real-time financial estimates.

Designed with production readiness in mind, this project breaks away from traditional, monolithic Jupyter Notebook prototypes. It introduces a decoupled architecture featuring a robust React/TypeScript client, a Node.js API orchestration layer, and a strictly isolated Python machine learning inference engine.

---

## Architectural Deep Dive

The repository is logically partitioned into three isolated domains, ensuring separation of concerns, independent scalability, and secure data flow.

### 1. Frontend Client (`/frontend`)
The client interface is a Single Page Application (SPA) built for resilience and a premium user experience.
* **Technology Stack:** React, TypeScript, Vite.
* **UI/UX Engineering:** Implemented a bespoke design system utilizing CSS glassmorphism, advanced typography, and modular card-based layouts. The interface avoids external CSS frameworks to demonstrate deep fundamental CSS knowledge.
* **Asynchronous Interactions:** Integrated `framer-motion` for declarative, hardware-accelerated animations (e.g., asynchronous result reveals).
* **State & Data Integrity:** Engineered robust asynchronous loading states to disable user interactions during network requests, preventing race conditions. Strict client-side form validation is enforced to guarantee that the backend receives only sanitized, strictly-typed payloads.

### 2. API Gateway (`/backend`)
The backend serves as a secure proxy and data orchestrator, shielding the Python ML environment from direct client-side requests.
* **Technology Stack:** Node.js, Express, TypeScript.
* **Dynamic Data Orchestration:** The API (`/api/cars/options`) serves hierarchical, conditionally-linked data to the client. By dynamically filtering available vehicle models based on the selected manufacturer, the system categorically prevents impossible data combinations (e.g., preventing the selection of a "Honda" manufacturer with a "Mustang" model).
* **Proxy Routing:** The `/api/cars/predict` endpoint validates incoming JSON payloads and securely proxies the data to the Flask inference engine, returning the serialized prediction back to the client.

### 3. Machine Learning Service (`/ml_service`)
The predictive core of the application, built with Python, Flask, Pandas, Scikit-Learn, and TensorFlow. To maintain a lightweight production environment, this service is divided into "Production" and "Research" environments.

#### Production Pipeline
* **Data Ingestion & Sanitization:** The `clean_data.py` script automates the transformation of raw data (`quikr_car.csv`) into a structured, normalized format (`Cleaned_Car_data.csv`).
* **Model Training & Serialization:** The `train_model.py` pipeline evaluates baseline and ensemble algorithms (including Decision Trees and Linear Regression). The optimal model is serialized into a byte-stream (`LinearRegressionModel.pkl`) for rapid deployment.
* **Inference API:** A lightweight Flask application (`app.py`) loads the `.pkl` file into memory at startup, exposing a REST endpoint that computes and returns sub-second price predictions.

#### Research & Development Lab (`/ml_service/research/`)
* **Exploratory Data Analysis (EDA):** Contains `Analysis.ipynb` for statistical visualization, feature engineering, and distribution analysis.
* **Deep Learning Experimentation:** Features `model_scratch.py`, a custom Feedforward Neural Network architected from scratch using TensorFlow and Keras. This environment allows for testing complex, multi-layer activation functions and backpropagation optimization without bloating the production server's dependency tree.

---

## Machine Learning Rigor & Validation

To ensure the models generalize well to unseen data and resist overfitting, several strict data science protocols were implemented:

* **K-Fold Cross-Validation:** The training pipeline abandons the standard, static train-test split. Instead, the dataset is partitioned into 'K' subsets, training and validating the model iteratively across multiple data folds. This guarantees consistent predictive accuracy regardless of data variance.
* **Statistical Error Metrics:** Model supremacy is determined through objective statistical evaluation rather than basic accuracy scores. The algorithms are heavily benchmarked using:
  * **Mean Squared Error (MSE):** To severely penalize large predictive outliers.
  * **R-squared (R²) Score:** To quantify the proportion of variance in the vehicle price that is predictable from the input features.
* **Algorithm Selection Matrix:** The architecture was finalized by directly comparing traditional statistical models against deep learning architectures. For this specific tabular dataset, the Scikit-Learn ensemble approach yielded optimal latency-to-error ratios for the production API, while the Neural Network remains available for complex, non-linear research.

---

## Codebase Structure

```text
car_price_predictor/
├── frontend/                 # React UI Client
│   ├── src/
│   │   ├── App.tsx           # Main application view and API integration
│   │   ├── App.css           # Custom glassmorphism design system
│   │   └── main.tsx          # React DOM entry point
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # Node.js API Gateway
│   ├── src/
│   │   └── index.ts          # Express server and proxy routing
│   ├── package.json
│   └── tsconfig.json
└── ml_service/               # Python ML Inference Engine
    ├── app.py                # Flask production API
    ├── clean_data.py         # Data sanitization pipeline
    ├── train_model.py        # Model training and serialization script
    ├── LinearRegressionModel.pkl # Serialized production model
    ├── Cleaned_Car_data.csv  # Sanitized dataset
    ├── requirements.txt      # Production dependencies
    └── research/             # Deep Learning Sandbox
        ├── Analysis.ipynb    # EDA and K-Fold visualization
        └── model_scratch.py  # TensorFlow/Keras Neural Network implementation

Local Deployment Guide
Due to the decoupled microservices architecture, the application requires three independent runtime environments.

Prerequisites
Node.js (v16.x or higher)

Python (3.8.x or higher)

pip and npm

Step 1: Initialize the Inference Engine (Flask)
Start the ML service first to ensure the API is ready to accept prediction requests.

Bash
cd ml_service

# Initialize a virtual environment for dependency isolation
python -m venv venv

# Activate the environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install strictly required production dependencies
pip install -r requirements.txt

# Boot the Flask inference server (Port 5000)
python app.py
Step 2: Initialize the API Gateway (Node.js)
Open a new terminal session to start the middle-tier orchestrator.

Bash
cd backend

# Install TypeScript and Express dependencies
npm install

# Boot the backend development server (Port 8080)
npm run dev
Step 3: Initialize the Client Interface (React/Vite)
Open a third terminal session to serve the frontend application.

Bash
cd frontend

# Install React, Framer Motion, and build dependencies
npm install

# Boot the Vite development server
npm run dev
Future Roadmap
Infrastructure as Code (IaC): Implement Dockerfile configurations for each service, unified by a docker-compose.yml file, enabling seamless, one-click containerized deployment.

Persistent Caching Layer: Integrate Redis within the Node.js gateway to cache identical prediction requests, significantly reducing the computational load on the Python inference engine.

Continuous Integration (CI/CD): Deploy GitHub Actions to enforce automated testing (PyTest for the ML pipeline, Jest for the Node.js backend) upon every commit to the main branch.
