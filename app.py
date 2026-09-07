import streamlit as st

# --------------------------------------------
# PAGE SETTINGS
# --------------------------------------------

st.set_page_config(
    page_title="Online Bookstore Assistant",
    page_icon="📚"
)

st.title("📚 Online Bookstore Assistant")
st.write("Find books by title, author, genre, price, language, or availability.")


# --------------------------------------------
# BOOK DATABASE
# --------------------------------------------

books = [
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "price": 450,
        "language": "English",
        "availability": "Available"
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genre": "Fiction",
        "price": 300,
        "language": "English",
        "availability": "Available"
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "Self-help",
        "price": 550,
        "language": "English",
        "availability": "Available"
    },
    {
        "title": "Wings of Fire",
        "author": "A.P.J. Abdul Kalam",
        "genre": "Biography",
        "price": 250,
        "language": "English",
        "availability": "Available"
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "Fantasy",
        "price": 400,
        "language": "English",
        "availability": "Out of Stock"
    }
]


# --------------------------------------------
# INTENT DETECTION
# --------------------------------------------

def detect_intent(message):

    message = message.lower()

    if any(word in message for word in ["hello", "hi", "hey", "good morning"]):
        return "GREETING"

    elif any(word in message for word in ["bye", "goodbye", "exit", "quit"]):
        return "GOODBYE"

    elif any(word in message for word in ["recommend", "suggest"]):
        return "RECOMMENDATION"

    elif any(word in message for word in ["available", "availability", "in stock", "stock"]):
        return "AVAILABILITY"

    elif any(word in message for word in ["author", "written by", "books by"]):
        return "AUTHOR"

    elif any(word in message for word in [
        "genre", "fantasy", "fiction", "biography", "self-help"
    ]):
        return "GENRE"

    elif any(word in message for word in [
        "price", "cost", "cheap", "expensive", "under", "below"
    ]):
        return "PRICE"

    else:
        return "BOOK_SEARCH"


# --------------------------------------------
# ENTITY EXTRACTION
# --------------------------------------------

def extract_entities(message):

    entities = {}
    message_lower = message.lower()

    authors = [
        "j.k. rowling",
        "paulo coelho",
        "james clear",
        "a.p.j. abdul kalam",
        "j.r.r. tolkien"
    ]

    for author in authors:
        if author.lower() in message_lower:
            entities["Author"] = author

    genres = ["fantasy", "fiction", "biography", "self-help"]

    for genre in genres:
        if genre in message_lower:
            entities["Genre"] = genre

    languages = ["english", "hindi"]

    for language in languages:
        if language in message_lower:
            entities["Language"] = language

    for book in books:
        if book["title"].lower() in message_lower:
            entities["Book"] = book["title"]

    words = message_lower.split()

    for i, word in enumerate(words):

        if word.isdigit():
            entities["Price"] = int(word)

        elif word in ["under", "below"] and i + 1 < len(words):
            if words[i + 1].isdigit():
                entities["Price"] = int(words[i + 1])

    return entities


# --------------------------------------------
# SEARCH BOOKS
# --------------------------------------------

def search_books(entities):

    results = books

    if "Book" in entities:
        results = [
            book for book in results
            if book["title"].lower() == entities["Book"].lower()
        ]

    if "Author" in entities:
        results = [
            book for book in results
            if book["author"].lower() == entities["Author"].lower()
        ]

    if "Genre" in entities:
        results = [
            book for book in results
            if book["genre"].lower() == entities["Genre"].lower()
        ]

    if "Language" in entities:
        results = [
            book for book in results
            if book["language"].lower() == entities["Language"].lower()
        ]

    if "Price" in entities:
        results = [
            book for book in results
            if book["price"] <= entities["Price"]
        ]

    return results


# --------------------------------------------
# CHATBOT RESPONSE
# --------------------------------------------

def chatbot_response(message, conversation):

    intent = detect_intent(message)

    entities = extract_entities(message)

    conversation.update(entities)

    if intent == "GREETING":

        return (
            "Hello! Welcome to the Online Bookstore Assistant. "
            "I can help you find books by title, author, genre, "
            "price, language, or availability."
        )

    elif intent == "GOODBYE":

        return "Thank you for using the Online Bookstore Assistant. Goodbye!"

    elif intent == "RECOMMENDATION":

        if not any(key in conversation for key in
                   ["Genre", "Author", "Price", "Language"]):

            return (
                "Sure! I can recommend a book. "
                "Could you tell me your preferred genre, author, "
                "language, or maximum price?"
            )

        results = search_books(conversation)

        if results:

            book = results[0]

            return (
                f"I recommend '{book['title']}' by {book['author']}.\n\n"
                f"Genre: {book['genre']}\n\n"
                f"Price: ₹{book['price']}\n\n"
                f"Language: {book['language']}\n\n"
                f"Availability: {book['availability']}"
            )

        return "I could not find a suitable recommendation."

    elif intent == "AUTHOR":

        if "Author" not in conversation:

            return "Sure. Which author's books are you looking for?"

        results = search_books(conversation)

        if results:

            response = "Books by " + conversation["Author"] + ":\n\n"

            for book in results:
                response += f"- {book['title']} (₹{book['price']})\n\n"

            return response

        return "Sorry, I could not find books by that author."

    elif intent == "GENRE":

        if "Genre" not in conversation:

            return (
                "Which genre would you like? "
                "For example: Fantasy, Fiction, Biography, or Self-help."
            )

        results = search_books(conversation)

        if results:

            response = f"Here are some {conversation['Genre']} books:\n\n"

            for book in results:
                response += (
                    f"- {book['title']} by {book['author']} "
                    f"(₹{book['price']})\n\n"
                )

            return response

        return "Sorry, I could not find books in that genre."

    elif intent == "PRICE":

        if "Price" not in conversation:

            return "What is your maximum budget for the book?"

        results = search_books(conversation)

        if results:

            response = f"Books available under ₹{conversation['Price']}:\n\n"

            for book in results:
                response += f"- {book['title']} - ₹{book['price']}\n\n"

            return response

        return "Sorry, I could not find books within that price range."

    elif intent == "AVAILABILITY":

        if "Book" not in conversation:

            return "Which book would you like me to check for availability?"

        results = search_books(conversation)

        if results:

            book = results[0]

            return (
                f"'{book['title']}' is currently "
                f"{book['availability']}."
            )

        return "Sorry, I could not find that book."

    else:

        if not any(key in conversation for key in
                   ["Book", "Author", "Genre", "Price", "Language"]):

            return (
                "I'd be happy to help you find a book. "
                "Could you tell me the title, author, genre, "
                "language, or your budget?"
            )

        results = search_books(conversation)

        if results:

            response = "I found these books:\n\n"

            for book in results:
                response += (
                    f"- {book['title']} by {book['author']} "
                    f"- ₹{book['price']} "
                    f"- {book['availability']}\n\n"
                )

            return response

        return (
            "Sorry, I could not find a book matching your requirements."
        )


# --------------------------------------------
# STREAMLIT CHAT MEMORY
# --------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = {}


# --------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# --------------------------------------------
# USER INPUT
# --------------------------------------------

user_input = st.chat_input("Type your message here...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = chatbot_response(
        user_input,
        st.session_state.conversation
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
