#!/bin/sh

# set BILLING_ACCOUNT_ID to one of your billing accounts
BILLING_ACCOUNT_ID=`gcloud beta billing accounts list | grep ACCOUNT_ID | cut -d ' ' -f2 | head -1`

RANDOM_SEED=`tr -dc a-z0-9 </dev/urandom | head -c 10`
PROJECT_ID=twitter-bot-$RANDOM_SEED

# Create a GCP project
gcloud projects create $PROJECT_ID --name="Twitter bot"

gcloud config set project $PROJECT_ID

gcloud beta billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT_ID

python3 resume-setup.py