# Twitter profile likes downloader (only media)

Downloads your twitter likes media (will discard text) locally using sellenium (no need for API credentials, only your user and password)

## install

Install requirements.txt
Install ffmpeg
run 
```
python -m seleniumwire extractcert
```

It will generate a .crt file, install it by doubleclicking on it
It will make your sellenium browser look legit for twitter.

## run

Run ``` python main.py``` it will ask you to give your user and password once
If you need to modify your user and password simply delete the file settings.ini

tweets saved will be stored in posts.db if you need to reset the already downloaded just delete the file posts.db

## Known bugs


## TODO:

- test headless mode
- add options thru a terminal menu to choose likes page or any other page
