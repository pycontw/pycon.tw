# Proposal Review System Documentation

Please refer to [PyCon TW Reviewer Guidebook](https://pycontw.github.io/reviewer-guidebook/)
for the description of the three-phase review process.  This README serves as instructions
for the succeeding Development Committee and Program Committee of PyCon Taiwan or any
conference who'd like to adapt the review system we use.

## Review Agenda

There are several time periods during the whole Call for Proposals and Proposal Review:

1. Call for Proposals
2. Inviting Review Committee
3. First Round Review
4. Modification Stage
5. Second Round Review
6. Internal Decision
7. Announcement of Acceptance

Each time period has a set of settings that need to be set in the Django administration dashboard, or
some steps you might need to go through, which will be documented here.

### 1. Call for Proposals

In the administration dashboard, go to `Home > Django Registry > Entries` with corresponding `SLUG`.
`SLUG` is the corresponding string of the conference evet, e.g. `pycontw-2020` for 2020.
For example, if you are running the version of year 2020,
you may also access the console via `https://<host address>:8000/2020/admin/registry/entry/` for staging and production site,
and `http://localhost:8000/admin/registry/entry/` for local development site.
You should have the following variables
:

| Key                                | Value   |
| ---------------------------------- | ------- |
| SLUG.proposals.creatable           | True    |
| SLUG.proposals.editable            | True    |
| SLUG.proposals.withdrawable        | True    |
| SLUG.reviews.stage                 | 0       |
| SLUG.reviews.visible.to.submitters | False   |

See the commit message of commit `4c1a1fc400d00ad4be963c902d9a92325804d08e`
for more [dj-registry](https://pypi.org/project/dj-registry/) information.

### 2. Inviting Review Committee

Inviting Review Committee is basically independent from the review process.  To promote a
user to become a reviewer, follow the steps below:

1. Go to `Django Admin > Users`, and find the reviewer's account with his/her email
2. In `Change User` page, go to `Permissions > Groups`, and add `Reviewer` group for the user

### 3. First Round Review

Before the review starts, Program Committee might want to check if there's any problematic
proposals, such as empty ones, repeated ones, or violating Code of Conduct etc.  So at the
moment the following settings are changed:

| Key                                | Value    |
| ---------------------------------- | -------- |
| SLUG.proposals.creatable           | False    |
| SLUG.proposals.editable            | False    |
| SLUG.proposals.withdrawable        | False    |
| SLUG.reviews.stage                 | 0        |
| SLUG.reviews.visible.to.submitters | False    |

When Program Committee is ready to start first round review, do the following change:

| Key                                | Value    |
| ---------------------------------- | -------- |
| SLUG.proposals.creatable           | False    |
| SLUG.proposals.editable            | False    |
| SLUG.proposals.withdrawable        | False    |
| SLUG.reviews.stage                 | 1        |
| SLUG.reviews.visible.to.submitters | False    |

### 4. Modification Stage

Before the review schedule goes into modification stage, Program Committee is responsible
for filtering malicious comments, comments that violate CoC, or inappropriate in any
ways.  All the reviews by default are set to inappropriate, therefore:

1. Go through all the reviews, manually on Django Admin or export them onto a spreadsheet
2. Manually check `appropriateness` field in Django Admin, or make a SQL query that
   updates for selected IDs in reviews table

When Program Committee is ready to start modification stage, do the following change:

| Key                                | Value    |
| ---------------------------------- | -------- |
| SLUG.proposals.creatable           | False    |
| SLUG.proposals.editable            | True     |
| SLUG.proposals.withdrawable        | False    |
| SLUG.reviews.stage                 | 0        |
| SLUG.reviews.visible.to.submitters | True     |

### 5. Second Round Review

| Key                                | Value    |
| ---------------------------------- | -------- |
| SLUG.proposals.creatable           | False    |
| SLUG.proposals.editable            | False    |
| SLUG.proposals.withdrawable        | False    |
| SLUG.reviews.stage                 | 2        |
| SLUG.reviews.visible.to.submitters | False    |

### 6. Internal Decision

After Second Round Review, Program Committee is responsible for making the final
decision of acceptance.  But before announcing acceptance, the following settings should
be set:

| Key                                | Value    |
| ---------------------------------- | -------- |
| SLUG.proposals.creatable           | False    |
| SLUG.proposals.editable            | False    |
| SLUG.proposals.withdrawable        | False    |
| SLUG.reviews.stage                 | 0        |
| SLUG.reviews.visible.to.submitters | False    |

Then, based on scores and comments, Program Committee should have a list of accepted,
rejected and waiting proposals.  Set "Accepted" field to "Accepted", "Rejected" or None
if the proposal is accepted, rejected or undecided.

Meanwhile Program Committee will need to filter through comments as well.  Follow the
description in "Modification Stage".

### 7. Announcement of Acceptance

| Key                                | Value    |
| ---------------------------------- | -------- |
| SLUG.proposals.creatable           | False    |
| SLUG.proposals.editable            | True     |
| SLUG.proposals.withdrawable        | False    |
| SLUG.reviews.stage                 | 0        |
| SLUG.reviews.visible.to.submitters | True     |
