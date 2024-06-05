# BizCardX: Extracting Business Card Data with OCR

![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?logo=linkedin&style=social) [Elamparithi T](https://www.linkedin.com/in/elamparithi-t/)

## Overview

BizCardX is a comprehensive web application that demonstrates my proficiency in Python programming, Optical Character Recognition (OCR) using EasyOCR, and interactive web development with Streamlit. It showcases advanced skills in SQL and database management by storing and retrieving business card data from a MySQL database, and efficient data handling with Pandas for structured data organization. The application also highlights my ability to implement modular programming by separating database handling, OCR processing, and web interface into distinct modules, enhancing maintainability and scalability. Additionally, I utilized OpenCV for image processing to enhance visualization of extracted information. The project involved setting up a virtual environment, installing necessary dependencies, and running the Streamlit application, reflecting my understanding of modern development practices, including version control with Git. This project is a testament to my capabilities in integrating multiple technologies into a cohesive and functional application.

## Technologies Used
- Python
- easyOCR
- Streamlit
- MySQL
- Pandas

## Modules

1. `SQL_datahandler.py`: Handles all SQL operations using the `mysql-connector` module.
2. `OCR_website.py`: Streamlit application to upload, display, and modify business card data.
3. `OCR_processing.py`: Processes the business card image using easyOCR and extracts relevant information.

## Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server

### Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure MySQL Server is running and create a database:
    ```sql
    CREATE DATABASE BizcardXDB;
    ```

### Running the Application
1. Run the Streamlit application:
    ```bash
    streamlit run OCR_website.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

## Usage

1. **Home Page**: Provides an overview of the application and the technologies used.
2. **Upload & Extract**: Allows users to upload a business card image. The app processes the image to extract information and displays the data.
3. **Modify**: Enables users to update or delete the extracted data from the database.
4. **Secrets**: Added to gitignore to store SQL server credentials secred.
5. **main.py**: This module is only to start streamlit application and run "OCR_website.py".

## License
This project no License.
