import wikipedia


def fetch_wikipedia_summary(query):
    try:
        topic = query.lower().replace("tell me about", "").strip()
        summary = wikipedia.summary(topic, sentences=2)  # Fix: 'sentence' -> 'sentences'
        return f"According to Wikipedia: {summary}"

    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple topics found: {e.options[:3]}"  # 'e' is now used to display options

    except wikipedia.exceptions.HTTPTimeoutError as e:
        return f"Network timeout occurred. Please try again later. Error: {e}"

    except wikipedia.exceptions.HTTPError as e:
        return f"HTTP error occurred. Error: {e}"

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Unexpected error: {e}")
        return "Sorry, I can't fetch that from Wikipedia."
