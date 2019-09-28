import os
from operator import attrgetter

# Local imports
from summarizer import Summarizer

if __name__ == "__main__":

    s = Summarizer(
        selected_topics=["advanced"],
        include_premium=False,
        output_dir="advanced_tutorials",
    )

    for topic in s.topics:
        filename = f"{topic.name} tutorials.md"
        path = os.path.join(s.output_dir, filename)

        tutorials = sorted(
            (t for t in topic.tutorials if t.has_comments),  # Filter tutorials
            key=attrgetter("comments.count"),  # Sort by # comments
            reverse=True,
        )

        # Check that we've found tutorials matching our criteria
        assert len(tutorials) > 0

        print(f"\nWriting file `{path}`\n")

        with open(path, "w") as f:
            f.write(f"# {topic.name} tutorials from Real Python" + "\n\n")
            for tutorial in tutorials:
                f.write(tutorial.markdown_title + "\n\n")
                if tutorial.has_metadata_string:
                    f.write(tutorial.markdown_metadata_string + "\n\n")
                f.write(tutorial.markdown_introduction + "\n\n")
