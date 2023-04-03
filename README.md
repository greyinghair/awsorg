# AWS Organisations Query

[![CodeQL](https://github.com/greyinghair/template_python/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/greyinghair/template_python/actions/workflows/codeql-analysis.yml)
[![Python Lint](https://github.com/greyinghair/template_python/actions/workflows/python-lint.yaml/badge.svg?branch=main)](https://github.com/greyinghair/template_python/actions/workflows/python-lint.yaml)

## Intro

This script is for querying AWS Organisations for a list of account ID's. </br>
The out is both to screen as well as to csv in the same path that you run the script from. </br>

Output values include: </br>
  - Account ID
  - Account OU
  - Account Tags['OwnerName', 'route-domain', 'environment']


## Usage

It is assumed you run this from withtin Cloudshell, logged in with an AWS account which grants your permissions to query AWS org </br>
From within CloudShell: </br>
  - Create vritual env
    ```hcl
    python3 -m venv awsorg
    source awsorg/bin/activate
    ```
  - Install boto3
    ```pip install boto3```
  - Clone this repo
    ```git clone https://github.com/greyinghair/awsorg && cd awsorg```
