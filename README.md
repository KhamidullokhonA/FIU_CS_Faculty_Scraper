# FIU CS Faculty Directory & CSRankings Comparison Tool

A browser-based tool for collecting the Florida International University (FIU) School of Computing and Information Sciences faculty roster, retrieving FIU author records from CSRankings, and comparing the two lists to identify possible additions, removals, and matches.

The application uses **Flask and Python** to retrieve FIU faculty data and **JavaScript in the browser** to fetch CSRankings data directly from GitHub. You do **not** need to clone the CSRankings repository or download its CSV files manually.

## Features

- **FIU Faculty Scraper:** Fetch faculty records from the FIU WordPress REST API, including names, titles, and emails.
- **Faculty Search:** Filter the displayed FIU roster by name or title.
- **CSRankings Data:** Fetch `csrankings-a.csv` through `csrankings-z.csv` directly from the CSRankings GitHub repository, filtering for `Florida International University` and displaying each author's name and ORCID.
- **Roster Comparison:** Compare the FIU and CSRankings lists using normalized and fuzzy name matching, and show records found in both lists or only one source.
- **CSV Export:** Download the FIU faculty list, FIU CSRankings entries, or the comparison results.

## Project Structure

Organize the files as follows:

```text
project-folder/
├── app.py
├── scraper_fiu.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
└── templates/
    └── index.html
```

- `app.py` — Flask application, serves the webpage and provides the `/scrape` API endpoint.
- `scraper_fiu.py` — Python scraper for FIU's WordPress faculty records.
- `templates/index.html` — HTML, CSS, and JavaScript for the interface, direct CSRankings retrieval, comparison, and CSV exports.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — builds the Python application image.
- `compose.yaml` — runs the application with Docker and publishes port 5001.
- `.dockerignore` — excludes local virtual environments, Git history, and other unnecessary files.

> If your downloaded files have names such as `app(4).py`, `scraper_fiu(2).py`, or `index(2).html`, rename them to match the structure above. Flask's `render_template("index.html")` expects the HTML file under `templates/`.

## Prerequisites

For the recommended Docker setup:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running (or Docker Engine with Compose).
- Git to clone the repository, or download the project ZIP instead.
- Internet access to retrieve records from FIU and CSRankings GitHub.
- A modern web browser.

You **do not** need to install Python or create a virtual environment when using Docker.

## Installation and Running with Docker (Recommended)

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_FOLDER>
```

Replace the placeholders with the repository's actual URL and folder name. Alternatively, download the repository ZIP, extract it, and open a terminal in the extracted folder.

### 2. Build and start the app

Make sure Docker Desktop is running. From the folder containing `compose.yaml`, run:

```bash
docker compose up --build
```

This builds the Docker image (installing Python dependencies) and starts the Flask app. The terminal remains attached and displays container logs. Open:

**http://localhost:5001**

The site is available only while the app is running. Docker Compose does not automatically open a browser.

### 3. Run in the background instead (optional)

```bash
docker compose up --build -d && echo "Open your app: http://localhost:5001"
```

The `-d` flag starts the app in the background, so live container logs are hidden. The `echo` command prints the browser link in your terminal once the Compose command succeeds. It does not guarantee Flask is fully ready yet.

### 4. Subsequent starts

Once the image has been built, you can normally start the existing app without rebuilding:

```bash
docker compose up -d && echo "Open your app: http://localhost:5001"
```

After changing application code, `requirements.txt`, or the Dockerfile, rebuild the image:

```bash
docker compose up --build -d && echo "Open your app: http://localhost:5001"
```

These commands work in macOS/Linux shells and Windows PowerShell.

### 5. Stop, inspect, or troubleshoot

```bash
docker compose down
```

Stops and removes the Compose-managed containers. Other useful commands:

| Action | Command |
| --- | --- |
| Show running services | `docker compose ps` |
| View logs | `docker compose logs --tail=50` |
| Follow live logs | `docker compose logs -f` |
| Start in the foreground | `docker compose up` |
| Stop foreground mode | Press `Ctrl+C` |

If the page does not load, check `docker compose ps` and the logs. Verify that `compose.yaml` publishes `5001:5000` and Flask listens on `0.0.0.0:5000` inside the container.

## Run Without Docker (Optional)

If you prefer to run directly with Python, install Python 3.9+ and create a virtual environment.

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

On Windows PowerShell:

```powershell
py -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe app.py
```

Then open the local URL printed by Flask. The local Python port can differ from the Docker URL.

## How to Use

### 1. Pull FIU faculty data

Click **Run scrape** to request the latest faculty roster from FIU's WordPress API through the Flask `/scrape` endpoint. The page displays each matching faculty member's name, title, and email.

Use the search box to filter the roster. Click **Export CSV** to download `faculty_members.csv`.

### 2. Pull CSRankings data

Click **Pull CSRankings Data**. JavaScript downloads the 26 letter-partitioned CSV files from the `gh-pages` branch of the [CSRankings GitHub repository](https://github.com/emeryberger/CSrankings):

```text
https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings-a.csv
...
https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings-z.csv
```

The browser parses the files and keeps rows whose `affiliation` field exactly matches `Florida International University`. It displays the associated names and ORCIDs. Click **Export CSRankings CSV** to download `fiu_csranking.csv`.

**No local CSRankings clone, build commands, or backend CSRankings API are required.** The browser retrieves the CSV files directly.

### 3. Compare the rosters

Once both datasets have loaded, click **Compare Rosters**. The application shows:

- **On CSRankings, not in FIU scrape:** Possible removals or records needing review.
- **In FIU scrape, not on CSRankings:** Possible additions or records needing review.
- **In both:** Matched names across the two sources.

Click **Download diff CSV** to save `roster_comparison.csv`.

**Important:** These are candidates for manual review, not authoritative add/remove decisions. Differences may result from incomplete scraping, affiliation labeling, name variants, or fuzzy-matching errors.

## Data Flow

```text
FIU WordPress API
        |
        v
scraper_fiu.py  <-- Flask GET /scrape <-- Browser: Run scrape
        |                                       |
        +------------ FIU faculty data --------+
                                                |
CSRankings GitHub CSVs --> Browser JavaScript --+
                                                |
                                        Compare Rosters
                                                |
                                  Results + downloadable CSVs
```

### FIU source

The Python scraper reads paginated staff-member records from:

```text
https://www.cis.fiu.edu/wp-json/wp/v2/staff-member
```

It selects records with at least one of the configured WordPress staff category IDs (`543`, `544`, `545`, `549`, `550`, `551`). These IDs are maintained in `scraper_fiu.py`.

### CSRankings source

The frontend uses JavaScript `fetch()` requests to GitHub's raw CSV URLs and filters entries by affiliation. The retrieved records are held in browser memory for the current page session, rather than saved automatically on the server.

## API Endpoint

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serve the main HTML interface |
| GET | `/scrape` | Run the FIU faculty scraper and return a JSON response containing `success` and `professors`, or an error |

Example successful response structure:

```json
{
  "success": true,
  "professors": [
    {"Name": "Example Faculty", "Title": "Professor", "Email": "example@fiu.edu"}
  ]
}
```

The example record is illustrative, not a real scraped result.

## Notes and Limitations

- **Internet required:** Both FIU and GitHub must be accessible. The GitHub requests must also be permitted by the browser's cross-origin policies.
- **Partial CSRankings results:** The current frontend counts failed CSV downloads but can still display a partial list. Do not treat comparisons as complete if any shard failed.
- **FIU scrape errors:** The current scraper stops on any non-200 HTTP response, which can also yield an incomplete roster.
- **Name-matching accuracy:** The comparison uses fuzzy matching, so false matches and missed matches are possible. Review results manually before changing CSRankings records.
- **No publication metadata:** This app retrieves CSRankings author names and ORCIDs, not per-paper details or publication counts.
- **CSV files download on demand:** The webpage exports CSVs in the browser; Flask does not automatically save these exports. Running `python scraper_fiu.py` directly also writes `faculty_members.csv` to the user's Desktop, as configured in that script.
- **Local development:** The Docker configuration described here is intended for local use, not a hardened public deployment.

## Data Attribution

- FIU faculty data: [FIU School of Computing and Information Sciences](https://www.cis.fiu.edu/)
- CSRankings author data: [CSRankings GitHub repository](https://github.com/emeryberger/CSrankings)

This project is a comparison aid and is not an official FIU or CSRankings service.
