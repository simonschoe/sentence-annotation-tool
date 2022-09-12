## Setup Guide

1. Install [prodigy](https://prodi.gy/) using the licence key
```sh
python -m pip install prodigy -f https://{licence-key}@download.prodi.gy
```

2. Download and extract [ngrok](https://ngrok.com/)

3. Run `conversion_input.py` to convert `.xlsx`-based sentence sample to json format

4. Start multiple prodigy sessions on localhost
```sh
set PRODIGY_PORT=8080
python -m prodigy transformation_manual {dset-name} input/{fname} -F custom_manual.py
```
```sh
set PRODIGY_PORT=8081
python -m prodigy transformation_manual {dset-name} input/{fname} -F custom_manual.py
```
```sh
set PRODIGY_PORT=8082
python -m prodigy transformation_manual {dset-name} input/{fname} -F custom_manual.py
```
5. Execute `ngrok.exe`

6. Authenitacte with ngrok
```sh
ngrok config authtoken {authtoken} --config ngrok.yml
```

7. Start ngrok tunnels to expose local ports
```sh
ngrok start --config ngrok.yml --all
```
**Forwarded to:**
- https://transf-coder-1.ngrok.io
- https://transf-coder-2.ngrok.io
- https://transf-coder-3.ngrok.io

8. Save all annotated files
```sh
python -m prodigy db-out {dset-name} output
```

## User Guide

**Hotkeys:**
- Accept: a
- Save: cmd + s

## Prodigy Commands

View stats and list all datasets
```sh
python -m prodigy stats -l
```

Delete dataset from database
```sh
python -m prodigy drop {dataset}
```
