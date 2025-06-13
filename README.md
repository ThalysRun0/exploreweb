git clone <me>

```bash
cd exploreweb
# install venv
python -m venv exploreweb
# windows OS
#./exploreweb/Script/Activate.ps1
# linux os
source exploreweb/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### run

```bash
# use the url extraction
python ./main.py --help
```

usage: main.py [-h] [-d DEPTH] [-w] start_url  

Explore un site web et génère une arborescence tabulée.  

positional arguments:  
  start_url             URL de départ du site (ex: https://example.com)  

options:  
  -h, --help            show this help message and exit  
  -d DEPTH, --depth DEPTH  
                        Profondeur maximale d'exploration (défaut: 2)  
  -w, --ssl             Désactiver la vérification SSL (non recommandé, optionnel)  

### Annexe for futur purposes

```bash
# run large
streamlit run ./app.py

# run locally
streamlit run app.py --server.address=127.0.0.1
```

#### force run locally
Windows plateform  
```bash
# %userprofile%\.streamlit\config.toml
[server]
headless = true
address = "127.0.0.1"
```
