import requests
import os

CHROME_PATH = "/opt/google/chrome/chrome"
CHAPTER_NAMES = [
    "Personal Introduction",
    "Introduction",
    "Graph Theory",
    "Random Networks",
    "The Scale-Free Property",
    "The Barabasi-Albert Model",
    "Evolving Networks",
    "Degree Correlations",
    "Network Robustness",
    "Communities",
    "Spreading Phenomena",
    "Preface",
]


def get_raw_chapter(n):
    response = requests.get(
        "http://networksciencebook.com/translations/en/partials/ch-{0}.html".format(n)
    )
    return response.text


def process_chapter(raw_chapter):
    processed_chapter = """
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
            <link rel="stylesheet" type="text/css" href="../main.css">.
            <title>{0}</title>
        </head>
        <body>
            <div ng-mouseup="showSelectedText()">
                <article class="book-content ng-scope">
                    <div class="book-content-hug">
                        <div id="scrollcontainer" onload="machSchoeneGraphen()" du-scroll-container="" class="ng-scope">
                            {1}
                        </div>
                    </div>
                </article>
            </div>
        </body>
    </html>
    """.format(
        "Chapter {0} - {1}.html".format(n, CHAPTER_NAMES[n]),
        raw_chapter.replace("../../../", "http://networksciencebook.com/"),
    )
    return processed_chapter


def write_chapter(n, processed_chapter):
    with open(
        "./files/html/Chapter {0} - {1}.html".format(n, CHAPTER_NAMES[n]), "w"
    ) as f:
        f.write(processed_chapter)


def write_pdf(n, processed_chapter):
    out_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "./files/pdf/Chapter {0} - {1}.pdf".format(n, CHAPTER_NAMES[n]),
        )
    )
    in_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "./files/html/Chapter {0} - {1}.html".format(n, CHAPTER_NAMES[n]),
        )
    )
    command = '{0} --headless --print-to-pdf="{1}" "file://{2}"'.format(
        CHROME_PATH, out_path, in_path
    )
    print(command)
    os.system(command)


for n in range(12):
    print("Getting Chapter {0} - {1}".format(n, CHAPTER_NAMES[n]))
    raw_chapter = get_raw_chapter(n)
    processed_chapter = process_chapter(raw_chapter)
    write_chapter(n, processed_chapter)
    write_pdf(n, processed_chapter)
