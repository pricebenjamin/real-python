import os

# Local imports
from summarizer import Summarizer

if __name__ == "__main__":

    s = Summarizer(
        include_premium=False,  # Do not include premium content
        output_dir="advanced_ml_tutorials",  # Specify output directory
    )

    selected_tutorials = [
        tutorial
        for topic in s.topics  # Iterate over all topics
        for tutorial in topic.tutorials  # Iterate over all tutorials within the topic
        if "advanced" in tutorial.tag_names  # Check that tutorial is tagged `advanced`
        and "machine-learning"
        in tutorial.tag_names  # and also tagged `machine-learning`
    ]

    # Check that we've found tutorials matching our criteria
    assert len(selected_tutorials) > 0

    filename = "advanced_ml_tutorials.md"
    path = os.path.join(s.output_dir, filename)

    print(f"\nWriting file `{path}`\n")

    with open(path, "w") as f:
        # Main title for the output
        f.write(f"# Advanced ML tutorials from Real Python" + "\n\n")

        for tutorial in selected_tutorials:
            # Title of the tutorial
            f.write(tutorial.markdown_title + "\n\n")

            # Include author, date, tags, and comments, if available
            if tutorial.has_metadata_string:
                f.write(tutorial.markdown_metadata_string + "\n\n")

            # Write first few paragraphs of the tutorial
            f.write(tutorial.markdown_introduction + "\n\n")
