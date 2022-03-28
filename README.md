# gcloud-twitter-bot
Run a Twitter bot serverlessly on Google Cloud

## deployment instructions

1. Ensure you have an active billing account https://console.cloud.google.com/billing

This project was designed to run for free, since it's not scheduled to execute more often than the free tier of the used services allow. But you're going to need to link it to an active billing account anyway.

2. Clone this project into Google Cloud Shell https://shell.cloud.google.com/

```bash
git clone https://github.com/JaderDias/gcloud-twitter-bot.git
cd gcloud-twitter-bot
./setup.sh
```