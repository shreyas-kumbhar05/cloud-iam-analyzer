
# Cloud IAM Analyzer

Work in progress. A small Python tool to analyse IAM policies in the cloud.

## Problem

IAM policies within clouds specify who/what can access your resources. However can result in over permissive policies even though the JSON could be valid. It can be easy to miss any risky permissions when analysing lots of policies.

## Risks

Over permissive policies will cause more damage if credentials or workload is compromised. For example allowing all actions across all resources means the identity has a lot more access than a specific policy. We also need to take in to consideration explicit deny statements, conditions and how permissions behave for each provider.

## Solution

The aim of this project is to create a local static analysis tool. By reading the IAM policy definitions, normalising the data and applying reusable security rules. This should accept input of AWS IAM JSON, Azure RBAC JSON, GCP IAM JSON and Terraform definitions related to IAM.

The tool will have the following features:

1. Parse the policies for each provider and normalise the data.

2. Apply security rules to the normalised data.


3. Output results with severity, reason and remediation.
4. Risk scoring and JSON/HTML output.

5. Automated tests and CI checks.

The parser and analysis are currently being built.

## How to run

The tool is built and tested locally. No cloud account is needed.

Clone the repo and navigate in to the directory:

```bash

git clone git@github.com:shreyas-kumbhar05/cloud-iam-analyzer.git
cd cloud-iam-analyzer

```

Create and activate the virtual enviroment. Install dependencies:
```bash

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

If pre-commit is not installed in the environment, install it. Then run any existing checks and tests:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
python -m pytest
```
The parser and scanning is not fully implemented so there is not a complete command to scan policies at this time. Once the CLI is implemented steps will be added.

## Progress
- Repo created and Python testing enviroment.
- Common logger and basic CI workflow.
- Normalised policy data model.
- Next step is to implement the AWS IAM parser.


## Tools

- Python
- pytest
- pre-commit, Black, Ruff, isort.
- GitHub Actions
- Git and GitHub

## Learning
This project is helping me practice splitting out the parsing from the security analysis. An important thing to note is to ensure the normalised data retains the authorisation meaning. I will add to this as I come across issues when implementing and testing.

## Licence
This project uses the MIT licence. See [LICENSE](LICENSE) for more information.
