# Continuous Deployment on Staging Server

The following describes how to setup continuous deployment for staging server. This setup presumes the site administrators have site deployment practices based on the docker production deployment [document/deploy_docker_prod.md](/document/deploy_docker_prod.md).

## Requirements for Staging Server
The staging server should have the following installed:
- Docker 17.09+ (since we use `--chown` flag in the COPY directive)
- Docker Compose
- python3.6+
- [docker](https://pypi.org/project/docker/) SDK for python
- [docker-compose](https://pypi.org/project/docker-compose/) SDK for python


## Prerequisite for Site Administrators
- Gather Container Environment Variables as mention in [document/deploy_docker_prod.md](/document/deploy_docker_prod.md).
- Have a ssh user and secret file for accessing GCE instance (staging machine)
    - Secret file will be further encoded by base64
- Administrators github Ids
    - For CD workflow authorization

## Settings for Github Actions Workflow
After aboves steps, we have to add collected information to github actions setting.
Please configure as the following in project's setting:

| Level  | Type   | Name   | Value (example) | Remarks |
|-----------|------------|---------------|----------|------------|
| Repository | secrets | PRODUCTION_DOT_ENV_FILE | `DATABASE_URL=...`   |   multiline support      |
| Repository | secrets | GCE_USERNAME | cd_user  | user name for ssh {user_name}@staging.pycon.tw  |
| Repository | secrets | SSH_PRIVATE_KEY | `21xa312....`     |  base64 encoded of key-pair (`.pem` file) |
| Repository | variables | PROJECT_ADMINS | `["github_user_1", "github_user_2"]` | For example `["josix"]` |

Reference
- [Create a secret for a repository](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)
- [Create a variable for a repository](https://docs.github.com/en/actions/learn-github-actions/variables#creating-configuration-variables-for-a-repository)
- Create base64 encoded string for `key.pem`
    - `base64 -i key.pem` (mac)
    - `cat key.pem | base64` (linux)

## Review
### Events that triggers the pipeline
1. When the PR merges to `master`
    - no authorization needed, as PRs normally reviewed before merge
2. Manually [trigger](https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow#running-a-workflow) the CD workflow (By admins)
    - only for Administrator specify in repository's variable called *PROJECTS_ADMINS*

Why? CD workflow will directly access to the GCE instance, should prevent unwanted deployments from PRs or push. (As a deployment guardian)
