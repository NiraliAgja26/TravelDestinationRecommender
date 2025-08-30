# TravelDestinationRecommender

A web application built with Django to help users discover and save their next travel destinations.

## Table of Contents

- [About The Project](#about-the-project)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)

## About The Project

TravelDestinationRecommender is a dynamic web application designed to provide users with personalized travel destination suggestions. Users can explore a wide range of destinations, view details, and maintain a personalized list of their favorite places.

The frontend is built with HTML, CSS, and JavaScript, utilizing Bootstrap for styling. The backend is powered by the Django framework, handling user authentication, data management, and the recommendation logic.

## Key Features

- **Destination Discovery:** Browse through a comprehensive catalog of travel destinations.
- **Detailed Views:** Get more information about each destination, including descriptions and images.
- **User Authentication:** Secure user registration and login system.
- **Favorites System:** Users can add destinations to their personal favorites list for easy access. The "favorite" status can be toggled dynamically without a page reload, thanks to asynchronous JavaScript (AJAX).
- **Responsive Design:** A clean and responsive user interface that works on both desktop and mobile devices.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.8+
- pip
- `virtualenv` (recommended)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd TravelDestinationRecommender
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    (Note: A `requirements.txt` file should be created for this project. If it doesn't exist, you may need to install Django manually: `pip install Django`)
    ```sh
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```sh
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

## Usage

1.  Navigate to the registration page and create a new user account.
2.  Log in with your new credentials.
3.  Explore the list of available travel destinations.
4.  On a destination's detail page, click the "Add to Favorites" button to save it.
5.  The button will update to "Favorited". You can click it again to remove it from your list.
6.  View your favorited destinations on your profile page (if available).
