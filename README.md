# Folderfly
### bla bla

## Installation
> *NOTE: this projects requires [python](https://python.org) and pip installed on your system.*

**1. Create an application.**
Create a new app on the Nylas dashboard. Navigate to "Hosted Authentication" > "Callback URIs" and add `http://localhost:5000/oauth/exchange`.

**2. Clone this repo**
```shell
git clone https://github.com/AnnaCoding42/Folderfy.git
```

**3. Open backend**
```shell
cd ./src/backend
```

**4. Update secrets**
Rename the `.env.sample` file to `.env` (in `/src/backend`) and fill it with your secrets (more info in the file)

**5. Install requirements**
```shell
pip install -r requirements.txt
```

**6. Run**
```shell
python main.py
```
Open your browser on `http://localhost:5000` and enjoy the project!