# Paperwork Pilot

> An AI agent that watches a Gmail label for incoming forms, extracts form fields, pre-fills known details, and only asks the user to review uncertain information.

## Hackathon

Built for **AWS Agents for Humans** — **Everyday Agents** track.

## Problem

People repeatedly type the same personal details into forms received through email: name, address, date of birth, phone number, email, and more. The work is small each time, but collectively wastes time and attention.

## Solution

Paperwork Pilot runs in the background and monitors a dedicated Gmail label called `Forms`.

When a new email containing a form arrives, it:

1. Detects the new email and attached PDF or form link.
2. Extracts form fields using an AI agent built with the Strands Agents SDK.
3. Uses a stored demo profile to pre-fill known information.
4. Identifies missing or ambiguous fields.
5. Sends the user a review notification only when confirmation or additional information is needed.
6. Produces a finalized form-output record after the user reviews it.

## Who it is for

Students, families, and working adults who receive repeated school, clinic, housing-society, service, or administrative forms through Gmail.

## Key principle

The user should not have to upload a document into another application every time. The agent starts automatically when a relevant email arrives and involves the user only for a meaningful decision.

## Planned architecture

```text
Gmail "Forms" label
        ↓
Python background poller
        ↓
Strands Agent + Amazon Bedrock
        ↓
Extract fields → pre-fill profile → flag uncertainty
        ↓
React review page + email notification
        ↓
Finalized output + reminder record
```

## Tech stack

- Python
- Strands Agents SDK
- Amazon Bedrock
- Gmail via IMAP
- React + Vite
- FastAPI
- PDFPlumber / PyPDF
- SQLite or JSON for MVP data

## Current status

Initial project setup in progress.

## Privacy and safety

This public repository uses only fake demo data. It does not contain real identity documents, email passwords, AWS credentials, or personal profile data.

## License

MIT