from summarizer import Summarizer

if __name__ == "__main__":
    s = Summarizer()

    for topic in s.topics:
        print("=" * 20, topic.name, "=" * 20)
        for i, tutorial in enumerate(topic.tutorials):
            print(f"{i}: {tutorial.title}")
            try:
                print(f"    {tutorial.markdown_metadata_string}")
            except Exception as e:
                print(f"    Exception: {e}")
