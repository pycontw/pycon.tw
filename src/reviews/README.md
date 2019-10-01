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

Each time period has a set of settings that need to be set in src/pycontw2016/settings, or
some steps you might need to go through, which will be documented here.

### 1. Call for Proposals

`settings.py`:

```python
PROPOSALS_CREATABLE = True
PROPOSALS_EDITABLE = True
PROPOSALS_WITHDRAWABLE = True
REVIEWS_STAGE = 0
REVIEWS_VISIBLE_TO_SUBMITTERS = False
```

### 2. Inviting Review Committee

Inviting Review Committee is basically independent from the review process.  To promote a
user to become a reviewer, follow the steps below:

1. Go to Django Admin > Users, and find the reviewer's account with his/her email
2. In Change User page, go to Permissions > Groups, and add "Reviewer" group for the user

### 3. First Round Review

Before the review starts, Program Committee might want to check if there's any problematic
proposals, such as empty ones, repeated ones, or violating Code of Conduct etc.  So at the
moment the following settings are changed:

```python
PROPOSALS_CREATABLE = False
PROPOSALS_EDITABLE = False
PROPOSALS_WITHDRAWABLE = False
```

When Program Committee is ready to start first round review, do the following change:

```python
REVIEWS_STAGE = 1
```

### 4. Modification Stage

Before the review schedule goes into modification stage, Program Committee is responsible
for filtering malicious comments, comments that violate CoC, or inappropriate in any
ways.  All the reviews by default are set to inappropriate, therefore:

1. Go through all the reviews, manually on Django Admin or export them onto a spreadsheet
2. Manually check `appropriateness` field in Django Admin, or make a SQL query that
   updates for selected IDs in reviews table

When Program Committee is ready to start modification stage, do the following change:

```python
PROPOSALS_EDITABLE = True
REVIEWS_STAGE = 0
REVIEWS_VISIBLE_TO_SUBMITTERS = True
```

### 5. Second Round Review

```python
PROPOSALS_EDITABLE = False
REVIEWS_STAGE = 2
REVIEWS_VISIBLE_TO_SUBMITTERS = False
```

### 6. Internal Decision

After Second Round Review, Program Committee is responsible for making the final
decision of acceptance.  But before announcing acceptance, the following settings should
be set:

```python
REVIEWS_STAGE = 0
```

Then, based on scores and comments, Program Committee should have a list of accepted,
rejected and waiting proposals.  Set "Accepted" field to "Accepted", "Rejected" or None
if the proposal is accepted, rejected or undecided.

Meanwhile Program Committee will need to filter through comments as well.  Follow the
description in "Modification Stage".

### 7. Announcement of Acceptance

```python
PROPOSALS_EDITABLE = True
REVIEWS_VISIBLE_TO_SUBMITTERS = True
```