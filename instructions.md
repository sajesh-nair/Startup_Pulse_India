startup_pulse_india/
│
├── .venv/                      # Your uv virtual environment
├── data/
│   └── dpiit_startup_data.xlsx # Your raw/processed data file
│
├── notebook.ipynb              # For EDA (Exploratory Data Analysis)
├── app.py                      # The Streamlit dashboard
├── pyproject.toml              # Auto-managed by uv
└── README.md                   # Project documentation for LinkedIn


# initiallize the project
uv init

# 1. Ensure Python 3.12 is downloaded and registered by uv
uv python install 3.12

# 2. Create an isolated virtual environment (.venv) right in this directory
uv venv --python 3.12

# 3. Pin this directory to explicitly use Python 3.12
uv python pin 3.12

# 4. uv version
python --version

# 5. Install Packages
uv add pandas numpy matplotlib seaborn plotly jupyter ipykernel openpyxl streamlit