# GCP Deployer

## About
This is a tool to package a function code and all it's required libraries and deploy it to the cloud from 
the command line using gcloud SDK. The current code supports Cloud Functions Gen1 and Cloud Run Functions.

## Prerequisites
- **gcloud SDK installed**
- **GCP credentials**: All required IAM permissions to interact with GCP
- **Proper folder structure**: See the current file structure in the code

## Steps in the code
1. Get the required deployer
2. Evaluate the user's input
3. Package all required code to a temporary location
4. Deploy to the cloud
5. Add any required triggers. Currently GCS file drop and pubsub message triggering is supported 

## Customising the code to your environment
1. Copy the following files to your repo root: consts.py, deploy.py, deployers.py
2. Edit consts.py with your specific names, paths and default settings
3. Add any required dependencies to your python env
4. Run the command in command line
5. Add comments to this repo if something doesn't work
---

### Command line samples
```commandline
e.g. 1 - Cloud Functions Gen1 with pubsub trigger
-- deploy function hello-http to project someproject with 360s runtime limit with max 5 instances and 1G memory
-- listen to messages coming on sometopic and map secret manager somesecret to env variable SOMEENVVAR
-- run tests and continue to deployment in case of no test failure
python -m deploy hello-http someprojectname CF -o 360 -i 5 -m 1024 -t sometopic -u -s SOMEENVVAR=somesecret:latest

e.g. 2 - Cloud Run Functions with GCS trigger
-- deploy function hello-gcs to project someproject with 180s runtime limit with max 5 instances and 512M memory and 2 cpu
-- listen to file drop events on bucket gs://somebucketname 
python -m deploy hello-gcs someproject CRF -o 180 -i 5 -m 512Mi -c 2 -b gs://somebucketname
