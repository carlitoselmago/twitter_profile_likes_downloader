# Twitter profile likes downloader (only media)

Downloads your twitter likes media (will discard text) locally using sellenium (no need for API credentials, only your user and password)

## install

Install requirements.txt

run 
```
python -m seleniumwire extractcert
```

It will generate a .crt file, install it by doubleclicking on it
It will make your sellenium browser look legit for twitter.

## run

Run ``` python main.py``` it will ask you to give your user and password once
If you need to modify your user and password simply delete the file settings.ini

## Known bugs

It downloads duplicates of videos to the wrong folders

## TODO:

- Move scroll to download all posts
- Check if already downloaded and skip