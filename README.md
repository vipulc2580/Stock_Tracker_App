# 📈 Real-Time Stock Tracker Web Application
  A dynamic web application that provides real-time stock price updates. Built with Django, Django Channels, Celery, and integrated with the Finnhub API, 
  this application offers users up-to-date stock information with real-time WebSocket communication.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Acknowledgements](#acknowledgements)

## Introduction
The Real-Time Stock Tracker Web Application is designed to provide users with live stock price updates. Leveraging Django's robust backend capabilities,
Django Channels for WebSocket support, Celery for asynchronous task management,and the Finnhub API for real-time stock data, this application ensures users have the latest stock information at their fingertips.

## Features
  - Real-Time Stock Updates: Receive live stock price updates every 10 seconds.
  - WebSocket Integration: Efficient real-time communication using Django Channels.
  - Asynchronous Task Management: Background tasks handled seamlessly with Celery.
  - User-Friendly Interface: Clean and intuitive UI for seamless user experience.
  - Stock Selection: Users can select specific stocks to track in real-time.

## Technologies Used
  ### Frontend:
   - HTML5
   -  CSS3
   - JavaScript
  ### Backend:
   - Python 3.x
   - Django Framework
   - Django Channels
   - Celery
  ### APIs & Libraries:
   - Finnhub API (for real-time stock data)
  ### Database:
   - SQLite (default Django database)
  ### Others:
   - Redis (as a message broker for Celery and Django Channels)

## Installation & Setup
 ### 1. Clone the Repository:
   ```bash
        git clone https://github.com/vipulc2580/Stock_Tracker_App.git
        cd Stock_Tracker_App
  ```

### 2. Create and Activate a Virtual Environment:
   ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

### 3. Install Dependencies:
  ```bash
        pip install -r requirements.txt
  ```

### 4. Apply Migrations:
  ```bash
        python manage.py migrate
  ```

### 5. Start Redis Server:
  - Ensure Redis is installed and running on your system.

### 6. Start Celery Worker:
  ``` bash
       celery -A stock_tracker worker --loglevel=info
  ```
### 7.Start Celery Beat:
  ```bash
       celery -A stock_tracker beat --loglevel=info
  ```
### 8. Run the Development Server:
  ```bash
       python manage.py runserver
  ```

### 9. Access the Application:
 - Open your web browser and navigate to http://127.0.0.1:8000/

## Usage
### User Journey:
- Select Stocks: Users can select specific stocks they wish to track.
- View Real-Time Updates: Once selected, the application provides live updates for the chosen stocks every 10 seconds.
- Interactive Dashboard: Users can view stock price changes in an organized and intuitive dashboard.

### Real-Time Functionality:
- WebSocket Communication: Utilizes Django Channels to establish a WebSocket connection for real-time data transmission.
- Background Tasks: Celery handles periodic tasks to fetch the latest stock data from the Finnhub API.
- Efficient Data Handling: Redis serves as the message broker, ensuring smooth communication between Django, Celery, and Channels.

## Screenshots
![InstaStock Banner Home](https://github.com/vipulc2580/Stock_Tracker_App/blob/main/screenshots/screenshot1.png)
![InstaStock Banner Track](https://github.com/vipulc2580/Stock_Tracker_App/blob/main/screenshots/screenshot2.png)


## Acknowledgements
- Django: For providing a robust web framework.
- Django Channels: For enabling WebSocket support in Django.
- Celery: For efficient asynchronous task management.
- Finnhub API: For providing real-time stock market data.
- Redis: For serving as a reliable message broker.
- Gratitude to the open-source community for continuous support and inspiration.
