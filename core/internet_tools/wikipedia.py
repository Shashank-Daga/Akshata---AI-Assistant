import wikipedia


def fetch_wikipedia_summary(query):
    try:
        for prefix in ["tell me about", "who is", "what is"]:
            if query.lower().startswith(prefix):
                topic = query.lower().replace(prefix, "").strip()
                break
        else:
            topic = query.strip()

        summary = wikipedia.summary(topic, sentences=2)
        return f"According to Wikipedia: {summary}"

    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple topics found: {e.options[:3]}"

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Sorry, I can't fetch that from Wikipedia."
