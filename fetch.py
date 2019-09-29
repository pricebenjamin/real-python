import argparse
import os
from operator import attrgetter

# Local imports
from summarizer import Summarizer

parser = argparse.ArgumentParser(
    description=(
        "Fetch introductory paragraphs (and information such as title, author, "
        "date, and tags) for all freely-available tutorials and courses on "
        "Real Python (https://realpython.com), then export this information "
        "into markdown."
    )
)

parser.add_argument(
    "selected_topics",
    metavar="topic",
    nargs="*",
    default="all",
    help="Only fetch tutorials / courses of the given topic(s) (default: 'all')",
)

parser.add_argument(
    "-o",
    "--output-dir",
    dest="output_dir",
    default="generated_markdown",
    help=(
        "Name of directory in which to store generated markdown files "
        "(default: 'generated_markdown')"
    ),
)

parser.add_argument(
    "-p",
    "--include-premium",
    dest="include_premium",
    action="store_true",
    help=(
        "Whether or not to include premium tutorials (a.k.a. courses) in "
        "generated files. (default: do not include premium)"
    ),
)

if __name__ == "__main__":

    args = parser.parse_args()

    summarizer = Summarizer(
        selected_topics=args.selected_topics,
        include_premium=args.include_premium,
        output_dir=args.output_dir,
    )

    for topic in summarizer.topics:
        # Write a separate file for each topic
        filename = f"{topic.name} tutorials and courses.md"

        path = os.path.join(summarizer.output_dir, filename)
        print(f"\nWriting file `{path}`\n")

        with open(path, "w") as f:
            # Main title of the file
            f.write(f"# {topic.name} tutorials and courses from Real Python" + "\n\n")

            for tutorial in topic.tutorials:
                # Title of the tutorial
                f.write(tutorial.markdown_title + "\n\n")

                # Include author, date, tags, and comment count (if available)
                if tutorial.has_metadata_string:
                    f.write(tutorial.markdown_metadata_string + "\n\n")

                # First few paragraphs of the article
                f.write(tutorial.markdown_introduction + "\n\n")
