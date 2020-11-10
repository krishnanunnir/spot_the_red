# Reddit Thread to Spotify

## What does it do?

Provide a reddit thread filled with musicals and it will automatically generate a spotify playlist for you. 

## How to run it?

Create a .env file based on the .ex-env.

```
cp .ex-env .env
```

Generate an app in Spotify and Reddit and add the different parameters in the .env file.

```
source .env
```

Now run it with the command

```
python3 start.py
```