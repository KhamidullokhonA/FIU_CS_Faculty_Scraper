from flask import Flask, render_template, jsonify
from scraper_fiu import scrape_faculty

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scrape")
def scrape():
    try:
        professors = scrape_faculty()

        return jsonify({
            "success": True,
            "professors": professors
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
