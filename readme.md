# ig-liker

Automatically likes your Instagram feed!

## Setup

Setup the Python environment with:

```bash
pip install requirements.txt
```

or, if using Conda, with:

```bash
conda env create --file=environment.yaml
conda activate ig-liker
```

Run the script with:

```bash
python main.py
```

## Command-line options

Option|Usage
-|-
`--username`|Instagram login. If not set, will be prompted.
`--password`|Instagram password. If not set, will be prompted.
`--stop-condition`|When the script should quit. Defaults to `5`. When more than `--stop-condition` posts have been encountered where each of them have already been liked, the script will quit.
`--period`|If set, the script will wait for `--period` seconds before running again. This will happen indefinitely.

The following flags should not be given a value:

Flag|Usage
-|-
`--headless`|If set, the chromedriver will be run in headless mode. This may cause additional errors, but will not launch a GUI.

For example, the following command will run the auto-liker every single day, after prompting for username and password exactly once:

```bash
python main.py --period=86400
```
