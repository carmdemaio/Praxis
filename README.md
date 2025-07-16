# Praxis Risk Engine
A Monte Carlo-based risk calculation tool built with FastAPI and Chart.js.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run API: `python praxis_api.py`
3. Open `index.html` in a browser.

* If you want to upload your own volatility calculation you will have to run both the frontend and backend on http://localhost (not file://).

Browsers treat file:// as a different origin, and CORS protection kicks in even if your FastAPI backend allows all origins. I've explicitly tried to do this in the code, but it is not possible. 

You can quickly run this on localhost by doing the following after installing python3:

cd ~/Praxis-main
python3 -m http.server 5500

Then open:
http://127.0.0.1:5500/index.html

## License
[MIT License](LICENSE)
