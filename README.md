# Tom and Jerry Object Detection – Dockerized Deployment

This project brings the **YOLOv11m-trained Tom & Jerry detector** from a previous project into production using **Flask**, **Docker**, and deployment on **AWS EC2**.  
Upload an image via the web interface, and the app will detect whether **Tom**, **Jerry**, or both appear in the image.  

---

## Features
- Detects **Tom** and **Jerry** in any uploaded image.  
- Simple **Flask web interface** for image upload & detection results.  
- Packaged in **Docker** for easy setup & reproducibility.  
- Deployable on **AWS EC2** (or any cloud/server that supports Docker).  

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/tom-jerry-detector.git
cd tom-jerry-detector
