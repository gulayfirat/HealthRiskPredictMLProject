# Health Risk Prediction ML Project

## 🌟 Project Description

This project is a **Machine Learning (ML) solution** developed to predict individuals' health risks based on lifestyle and health data **obtained from Kaggle**. The prediction service is offered as a RESTful API via a modern **FastAPI** server and includes a simple web interface (Jinja2).

## ✨ Features

* **ML Prediction:** High-accuracy risk classification using a trained `scikit-learn` model.
* **RESTful API:** A fast and scalable prediction interface using **FastAPI**.
* **Data Management:** Data reading and storage via the **SQLite** database (`Health_Risk.db`).
* **Web Interface:** A simple interface where users can enter prediction inputs and view results.

## 🛠️ Technologies

| Category | Technology | Description |
| :--- | :--- | :--- |
| **ML/Data** | `scikit-learn`, `pandas` | Model training and data manipulation. |
| **Database** | **SQLite** | Storage and management of project data. |
| **Web Framework** | `fastapi` | High-performance API service. |
| **Server** | `uvicorn` | ASGI web server. |
| **Templating** | `Jinja2` | Creating dynamic web pages. |

**(See `requirements.txt` for all dependencies.)**

## 🚀 Setup and Running

### 1. Install Dependencies

To install project dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run the Application
Run the main application using uvicorn:
```bash
uvicorn app:app --reload
```
### 3. Usage
The application will run on http://127.0.0.1:8000 by default.
* Web Interface: You can test the prediction via the visual interface by visiting http://127.0.0.1:8000/.
* API Documentation: You can access the automatically generated interactive API documentation (Swagger UI) at http://127.0.0.1:8000/docs.
### Dataset Source
https://www.kaggle.com/datasets/zahranusrat/lifestyle-and-health-risk-prediction-dataset

## ✨📸 Screenshot

<img width="300" height="400" alt="Screenshot 2025-11-19 at 19 50 44" src="https://github.com/user-attachments/assets/d01fab14-f34f-481b-a532-a270a61e98d5" />
<img width="300" height="400" alt="Screenshot 2025-11-19 at 19 51 31" src="https://github.com/user-attachments/assets/6fce6360-1acb-406d-9b04-13923367bb16" />
<img width="300" height="400" alt="Screenshot 2025-11-19 at 19 51 54" src="https://github.com/user-attachments/assets/4025cf39-edca-4dfa-bbd6-b9ca61a4de11" />

