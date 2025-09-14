-----

# 🎬 Movie Recommendation System

This project is a **Streamlit-based movie recommendation system** that suggests similar movies to a user's selection. It utilizes a pre-trained model for recommendations and fetches movie metadata like posters, ratings, and plots from the OMDb API. The app is deployed and accessible via a web link.

\<div align="center"\>
\<a href="[https://movierecommenderbypranav.streamlit.app](https://movierecommenderbypranav.streamlit.app)"\>
\<img src="[https://miro.medium.com/v2/resize:fit:1100/format:webp/1\*qR08Jxq0IHdvFtBsUhCe3Q.jpeg](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*qR08Jxq0IHdvFtBsUhCe3Q.jpeg)" alt="Movie Recommendation System Demo" width="700"/\>
\</a\>
\<br /\>
*Click the image to see a live demo\!*
\</div\>

-----

## ✨ Features

  * **Interactive UI**: A sleek, interactive user interface built with **Streamlit**.
  * **Movie Selection**: Users can select a movie from a dropdown list to get recommendations.
  * **Recommendations**: The system recommends five movies similar to the one selected.
  * **Movie Metadata**: Displays posters, years, ratings, genres, and plots for all recommended movies.
  * **Efficient Caching**: Uses in-memory and local file caching for movie metadata to improve performance and reduce API calls.
  * **Dynamic Data Loading**: The recommendation model's similarity matrix is loaded dynamically from a **Hugging Face dataset**, with a fallback to a local file.
  * **Responsive Design**: The web application is designed to be responsive, providing a good user experience on different screen sizes.

-----

## 🚀 Getting Started

### Prerequisites

  * **Python 3.x**
  * **pip**

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Pranav7378/MovieRecommender.git
    cd MovieRecommender
    ```

2.  **Install the required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the App

1.  **Set up your OMDb API key**:
    Create a `.streamlit/secrets.toml` file in your project directory and add your OMDb API key. You can get a free key by signing up on the [OMDb API website](https://www.omdbapi.com/apikey.aspx).

    ```toml
    # .streamlit/secrets.toml
    OMDB_KEY = "your_omdb_api_key_here"
    ```

2.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

The application will open in your default web browser.

-----

## 🛠️ Technology Stack

  * **Python**: The core language for the project.
  * **Streamlit**: For building the interactive web application.
  * **Pandas**: For data manipulation (reading movie data).
  * **Pickle**: For serializing and deserializing the movie data and similarity matrix.
  * **Requests**: For fetching movie metadata from the OMDb API and the similarity matrix from Hugging Face.
  * **OMDb API**: The source for movie metadata (posters, ratings, plots, etc.).
  * **Hugging Face Datasets**: Used to host the `similarity.pkl` file, allowing for easy remote loading.