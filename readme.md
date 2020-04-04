# ig-liker

Automatically likes posts on your Instagram feed!

## Setup

Setup the Python environment with:

```bash
pip install -r requirements.txt
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

### Headless Ubuntu

Chromedriver can be run headless on Ubuntu after installing Chrome and several dependencies:

```bash
sudo apt-get install libxss1 libappindicator1 libindicator7;
sudo apt --fix-broken install;
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb;
sudo dpkg -i google-chrome*.deb;
rm google-chrome*.deb;
sudo apt-get install -f;
sudo apt-get install xvfb;
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

## Changelog

### 1.0.2

* Fixed typo in `readme`.

### 1.0.1

* Added instructions for headless Ubuntu.

### 1.0.0

* Login works again.
* Does not like comments anymore.
