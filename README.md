# FastAPI File Sharing Application

This is a **FastAPI** web application that serves as a platform for sharing files between a server and a client. The application creates `uploads` and `downloads` directories on the running directory, enabling seamless file sharing via a web browser.

---

## Features
- **File Download:** Clients can access and download files placed in the `uploads` folder on the server by opening the URL in a web browser (`http://<server_ip>:<port>`).
- **File Upload:** Clients can upload files via the browser, and the uploaded files will be placed in the `downloads` folder on the server.

---

## Requirements
- **Python**: Version 3.12 or higher
- **Docker** (optional, for containerized deployment)

---

**Note:** This repo has been tested only on Ubuntu 24.04.

---

## Installation and Running the Application

### 1. Clone the Repository
```bash
git clone https://github.com/Alikavari/sharefile.git
cd  sharefile
```
### 2. Follow one of A or B installation and running method 

#### A. Normal Installation

##### For Linux/MacOS Users
1. Create a virtual environment:
   ```bash
   python3 -m venv myenv
   ```
2. Activate the virtual environment:
   ```bash
   source myenv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Navigate to the `sharefile` directory:
   ```bash
   cd sharefile
   ```
5. Run the application:
   ```bash
   uvicorn shareFile:app --host 0.0.0.0 --port 8000 --reload
   ```

##### For Windows Users
1. Create a virtual environment:
   ```cmd
   python -m venv myenv
   ```
2. Activate the virtual environment:
   ```cmd
   myenv\Scripts\activate
   ```
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Navigate to the `sharefile` directory:
   ```cmd
   cd sharefile
   ```
5. Run the application:
   ```cmd
   uvicorn shareFile:app --host 0.0.0.0 --port 8000 --reload
   ```

#### B. Using Docker

##### For Linux/MacOS Users
1. Build the Docker image:
   ```bash
   docker build -t sharefile-app .
   ```
2. Run the Docker container:
   ```bash
   docker run -it --rm -p 8000:8000 -v $(pwd):/app sharefile-app
   ```

##### For Windows Users
1. Build the Docker image:
   ```cmd
   docker build -t sharefile-app .
   ```
2. Run the Docker container:
   ```cmd
   docker run -it --rm -p 8000:8000 -v %cd%:/app sharefile-app
   ```

---

## Usage
1. **Access the Application:**
   Open your browser and navigate to `http://<server_ip>:8000`.

2. **File Sharing:**
   - Place files in the `uploads` folder for clients to download.
   - Clients can upload files, and the uploaded files will be stored in the `downloads` folder.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

