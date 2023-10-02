# Continuous Deployment on Staging Server

The following describes how to setup continuous deployment for staging server. This setup presumes the site administrators have site deployment practices based on the docker production deployment [document/deploy_docker_prod.md](/document/deploy_docker_prod.md).

# Introduction of CI/CD, GitHub Actions, Ansible and related settings
Continuous integration (CI)
- Refers to the build and unit testing stages of the software release process. Every revision that is committed triggers an automated build and test.

Continuous delivery / Continuous Deployment (CD)
- Usually as the next step for Continuous Integration, the code revision is built and tested in the application is automatically released to the production environment.

GitHub Actions
- A CI/CD platform or service provided by GitHub. It provides public runners with limited compute minutes to run CI/CD workflows defined at `.github/workflows` directory. We can also provision custom Github Actions runner to perform CI/CD task.

Ansible
- An automation tool that utilize *playbook* and *inventory* to manage production servers (nodes), such as sending commands, file transfers, system maintenance without manually setup via SSH/Remote session for it.

Github Settings for secrets and variables
- CI/CD workflows for Github Actions often obtain sensitive information, credentials or variable. In project settings, Github provides secrets vault and variable holder to store these information in the secure manner and able to retrieve and use these values when the workflows run.

## High level comparison of CI/CD in this project
| Conventional - Release | Github Actions + Ansible - Release |
|-----------|------------|
| `ENV` values managed by site admin | `ENV` values are set in project settings (secrets) |
| Site admin solely manage the production server | Site admin gives rights to github actions to deploy release to the production server |
| Site admin knows every deployment steps for docker | Deployment steps are defined in Ansible playbook (so everyone can understand deployment steps) |
| Site admin runs commands in a SSH session | Ansible runs the commands to server as defined by the playbook |
| Only admins have the server IP and private key | Server IP and private key are securely kept at github settings |
| Release is manual | Release automatically once code merges to `master` branch |
| Things are executed by hands | Things are executed by Github Actions' runner |

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
After aboves steps, we have to add collected information to Github actions setting.

Under the hood, we github action and [Ansible](https://www.ansible.com/overview/how-ansible-works) for continuous deployment. Github action will hold necessary variables and secrets that allows Ansible to access the staging VM on your behalf.

So kindly configure project's action setting as the following:

| Level  | Type   | Name   | Value (example) | Remarks |
|-----------|------------|---------------|----------|------------|
| Repository | secrets | PRODUCTION_DOT_ENV_FILE | `DATABASE_URL=...`   |   multiline support      |
| Repository | secrets | PRODUCTION_GOOGLE_CLOUD_STORAGE_JSON | `{ ...`   |   multiline support      |
| Repository | secrets | VM_USERNAME | cd_user  | user name for ssh {user_name}@{vm_domain}  |
| Repository | secrets | VM_DOMAIN_IP | staging.pycon.tw  | IP address or Domain that points to the staging server  |
| Repository | secrets | VM_PYTHON_INTERPRETER | `/home/dev/.pyenv/shims/python`  | path to your python environment that has docker/docker-compose packages installed |
| Repository | secrets | SSH_PRIVATE_KEY | `21xa312....`     |  base64 encoded of key-pair (`.pem` file) |
| Repository | variables | PROJECT_ADMINS | `["github_user_1", "github_user_2"]` | For example `["josix"]` |

Reference
- [Create a secret for a repository](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)
- [Create a variable for a repository](https://docs.github.com/en/actions/learn-github-actions/variables#creating-configuration-variables-for-a-repository)
- Create base64 encoded string for `key.pem`
    - `base64 -i key.pem` (mac)
    - `cat key.pem | base64` (linux)

## CD Workflow Rules
### Events that triggers the pipeline
1. When the PR merges to `master`
    - no authorization needed, as PRs normally reviewed before merge
2. Manually [trigger](https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow#running-a-workflow) the CD workflow (By admins)
    - only for Administrator specify in repository's variable called *PROJECTS_ADMINS*

Why? CD workflow will directly access to the GCE instance, should prevent unwanted deployments from PRs or push. (As a deployment guardian)
