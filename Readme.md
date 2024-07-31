---

## _Stori Challenge_

#### _Alejandro Herrera_

For this project, the main milestone is to process, summarize, and send account transactions (TXN) to the final user.

- The summary email will include monthly details.
- Include the generated CSV file.
- The code is versioned in a Git repository. The README.md file should describe the code interface and provide instructions on how to execute the code.

## Features

- Lambda to dynamically generate the TXN file; only provide the email to send.
- Lambda to process and summarize the transactions, creating a JSON payload.
- Lambda to format the JSON payload as an email and send it.
- Lambda to store the TXN into a DynamoDB.

## Notes

For the transaction format, complete the date format for each transaction:

| id  | date        | transaction |
|-----|-------------|-------------|
| 15  | 2024/01/07  | +4054.33    |

Once generated, the file is dropped into a folder called `shared_data` to be processed locally or uploaded to the S3 bucket created by the project.

## Tech

For this project, I am using:

- [Python] - To write the code for the Lambdas.
- [Serverless] - To deploy and manage the infrastructure via CloudFormation.
- [Docker] - To deploy locally.

## Requirements

```
- Docker
- SMTP server credentials
- AWS credentials with permission to deploy
```

## Environment Variables

For correct deployment, create your own `.env` file. An `env.example` file is provided; just copy and rename it to `.env`, and add your own credentials.

```sh
# The stage for local dev purposes. If you want to deploy to AWS, use an appropriate stage name: live, staging, etc.
STAGE=local

AWS_DEFAULT_REGION="us-east-1"
# The credentials from AWS
AWS_ACCESS_KEY_ID=AKIA
AWS_SECRET_ACCESS_KEY=SECRETKEY
# The S3 bucket naming is global for all accounts, we set a postfix to prevent duplication
POSTFIX_RANDOM=anRandomWord
# SMTP CONFIG
SENDER_EMAIL=challenge_stori@talachas.dev
USE_TLS=1
SMTP_HOST=sandbox.smtp.mailtrap.io
SMTP_PORT=587
SMTP_USER=USER
SMTP_USER_PASSWORD=PASS
```

## Installation

All the commands are simplified using a Makefile. [Makefile tutorial](https://makefiletutorial.com/#why-do-makefiles-exist)

#### Build

```sh
make run-local
```

#### Generate the TXN file

This will generate a CSV file with the transactions.

```sh
make generate-txn EMAIL=the_fancy_email@example.com
```

#### Test POC project

A simple file uploader to upload the txn is here upload the file to the S3 of the APP, and run the process
ans send the email from

challenge_stori@gmail.com

```
https://b9egukwy4h.execute-api.us-east-1.amazonaws.com/file_upload

```



### Deploy
For AWS environments, it's important to change the `STAGE` variable from ".env" to something different.

If you want to deploy, change the `STAGE` environment variable to "test" or "stage".

```sh
make deploy
```

### Clean up

```sh
make destroy
```

---




