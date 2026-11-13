# discussion-board-with-user-authentication-and-wellness-dashboard
A Python and Streamlit-based healthcare platform featuring a public discussion board, user authentication, private wellness dashboard, personal journaling, wellness check-ins, and physical health tracking, powered by SQLite.
Discussion Board with User Authentication and Wellness Dashboard

Project Overview

A caregiver support and wellness platform developed using Python, Streamlit, and SQLite.

The application combines a public discussion board with authenticated user accounts and a private wellness dashboard. Its purpose is to provide caregivers with a space to connect with others while also supporting individual wellness tracking and personal reflection.

Platform Architecture

The application is organized into three primary components:

1. Community Discussion Board

A public-facing discussion environment that allows users to:

Create discussion posts.

Browse community discussions.

Comment on existing posts.

Read and engage with shared experiences.

2. User Authentication

An account management system that provides:

User registration.

Username and email collection.

Password hashing and verification.

Login and logout functionality.

Session-based user identification.

Passwords are protected using salted PBKDF2-HMAC-SHA256 hashing.

3. Private Wellness Dashboard

An authenticated user environment containing three primary features.

Private Diary

Create personal journal entries.

Automatically record entry timestamps.

View, edit, and delete previous entries.

Associate entries with individual user accounts.

Wellness Check-In

Record mood.

Rate stress levels on a 1–10 scale.

Record physical wellness.

Add optional notes.

Review previous check-ins.

Physical Health Tracker

Track hours of sleep.

Record physical activity minutes.

Rate energy levels on a 1–10 scale.

Add optional notes.

Review historical physical health records.

Technical Architecture

Component

Technology

Programming Language

Python

Application Framework

Streamlit

Database

SQLite

Password Hashing

hashlib / PBKDF2-HMAC-SHA256

Password Verification

hmac

Development Environment

Jupyter Notebook

Operating Environment

Windows

Database Structure

The application currently uses a SQLite database named discussion_board.db.

The database contains the following tables:

Table

Purpose

users

Account registration and authentication

discussions

Public community posts

comments

Discussion comments

wellness_checkins

Private wellness assessments

diary_entries

Private personal journal entries

physical_health

Individual physical health records

Private wellness records are associated with user IDs to support separation between individual accounts.

Information Flow

Community

User accesses the discussion board.

User creates or views discussions.

Users contribute comments.

Discussion information is stored in SQLite.

Private Wellness

User registers an account.

Password is hashed and stored.

User authenticates through the login system.

The application establishes a user session.

User accesses the private wellness dashboard.

Personal information is stored and retrieved using the authenticated user's ID.

Current Development Status

Public discussion board

Discussion creation

Community comments

User registration

Password hashing

User login and logout

Private wellness dashboard

Private diary with editing and deletion

Wellness check-ins

Wellness check-in history

Physical health tracking

Physical health history

Future Development

Planned improvements include:

User interface redesign and branding.

Improved dashboard navigation.

Wellness summaries and historical visualizations.

Additional personal wellness features.

Community engagement enhancements.

Secure deployment and production infrastructure.

Expanded privacy and security controls.

Security and Privacy Considerations

This project is currently an early-stage prototype.

Although password hashing and user-specific database queries have been implemented, additional security controls, authentication hardening, authorization testing, encryption, secure hosting, and privacy review are required before production deployment.

The application is not currently intended for storing real users' sensitive health information.

Development Philosophy

The platform is being developed incrementally, with an emphasis on functional application development, data organization, user experience, and privacy-conscious architecture.

Project Name: The Caregiver Circle
Development Status: Active Prototype
Primary Technologies: Python, Streamlit, SQLite
