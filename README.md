# PRS-I : AI-Based Product Review System

## Introduction
This project is a cutting-edge product review analysis tool leveraging Natural Language Processing (NLP) to assess the sentiment of product reviews. The backend is built with Django, while the frontend is crafted using vanilla HTML, CSS, and JavaScript. The NLP model, developed with the NLTK library, predicts the sentiment of product reviews.

## Demo

# Product Review analyzer
![Demo Image](![image](https://github.com/sahilshukla3003/AI-Based-Product-Review-System-PRS-I-/assets/124785012/4a486a48-6842-4bac-87d4-a50b2ea4731e)
)

# Personalized Reviews
![Demo Image](![image](https://github.com/sahilshukla3003/AI-Based-Product-Review-System-PRS-I-/assets/124785012/6e475305-71ff-45b2-97d0-1ae77637842f)
)

## Features
- **Product Link Entry:** Users can input a product link, and the review text is automatically extracted from product pages on platforms such as Amazon and Flipkart.
- **Sentiment Analysis:** The extracted review text undergoes analysis to determine its sentiment.
- **Sentiment Display:** The sentiment analysis results are presented to the user, accompanied by a summarized review and a visual representation of the sentiment.
- **Personalized Reviews:** Users can receive personalized reviews based on their past preferences and review history.

## Review Scope
The AI product reviewer harnesses NLP techniques to:
- Extract and process review text from various product pages.
- Analyze and predict the sentiment of the reviews.
- Provide users with comprehensive summaries and visual sentiment representations.
- Offer personalized review recommendations based on user history.

## Components

### Chrome Extension (Entry Point)
The Chrome extension serves as the entry point, allowing users to effortlessly extract review text from product pages on major e-commerce platforms.

### Main Website
- **User Authentication:** Secure authentication for managing user accounts.
- **User History:** Maintains a detailed history of analyzed reviews for each user.
- **Personalized Reviews:** Delivers personalized review summaries and suggestions based on user preferences and past interactions.

### REST API
The REST API connects the Chrome extension to the backend, handling:
- Requests for review text extraction.
- Communication with the NLP model for sentiment analysis.
- Storage and retrieval of user history, authentication data, and personalized review data.

### NLP Model
The NLP model, developed using the NLTK library, processes review texts to:
- Clean and tokenize the text.
- Analyze sentiment using pre-trained models and custom algorithms.
- Generate sentiment scores and summaries for the reviews.

### Database
A robust database system is used to:
- Store user authentication details.
- Maintain a history of analyzed reviews for each user.
- Save sentiment analysis results, summaries, and personalized review data.

## Installation

### Prerequisites
- Python 3.x
- Django
- NLTK
- HTML, CSS, JavaScript
- Chrome browser (for extension)

### Steps
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-repo/AI-Product-Review-System.git
   ```
2. **Backend Setup:**
   - Navigate to the backend directory.
   - Install the required Python packages:
     ```sh
     pip install -r requirements.txt
     ```
   - Run database migrations:
     ```sh
     python manage.py migrate
     ```
   - Start the Django server:
     ```sh
     python manage.py runserver
     ```
3. **Frontend Setup:**
   - Open the frontend directory.
   - Serve the HTML file or set up a local server to view the frontend.
4. **Chrome Extension:**
   - Load the Chrome extension by navigating to `chrome://extensions/`.
   - Enable Developer mode.
   - Click "Load unpacked" and select the extension directory.

## Usage
1. **Open the Chrome Extension:**
   - Enter the product page URL.
   - Extract review text.
2. **Analyze Review:**
   - The review text is sent to the backend for sentiment analysis.
3. **View Results:**
   - The sentiment, summary, and graphical representation are displayed on the main website.
4. **Personalized Reviews:**
   - Users can view personalized review recommendations based on their previous interactions and preferences.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any queries or support, contact us at [sahilshukla959@gmail.com].

---

Feel free to customize this README as per your project's specifics and add any additional sections that might be necessary.
