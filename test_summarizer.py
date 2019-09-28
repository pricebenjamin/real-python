import os
from operator import attrgetter

# Local imports
from summarizer import Summarizer

if __name__ == "__main__":

    s = Summarizer(selected_topics="all", include_premium=True, output_dir="test_md")

    for topic in s.topics:

        filename = f"{topic.name} tutorials and courses.md"
        path = os.path.join(s.output_dir, filename)

        print(f"    Writing file `{path}`")
        with open(path, "w") as f:
            f.write(f"# {topic.name} tutorials and courses from Real Python" + "\n\n")

            for tutorial in topic.tutorials:
                f.write(tutorial.markdown_title + "\n\n")
                if tutorial.has_metadata_string:
                    f.write(tutorial.markdown_metadata_string + "\n\n")
                f.write(tutorial.markdown_introduction + "\n\n")
