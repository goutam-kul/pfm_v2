# Personal Finance Manager (PFM) Version-2

## Overview
Personal Finance Manager v2 is the successor to the original Personal Finance Manager project. This new version introduces major improvements and additional features aimed at providing a more secure, user-friendly, and robust system for managing personal finances. 

## Major Changes in v2

### 1. Database Migration to PostgreSQL
- The database has been migrated from SQLite to PostgreSQL, providing better performance, scalability, and support for advanced queries.

### 2. User Management
- **User Accounts**: Users can now create their own accounts with a unique user ID and password.
- **Login System**: Users can securely log in to their accounts.
- **Token-Based Authentication**: All API requests are secured using token-based authentication.
- **Password Reset with OTP**: Users can reset their passwords by verifying their identity through an OTP sent to their registered email.

### 3. Expense Management
- **Add Expenses**: Users can log their expenses by providing details such as category, amount, and date.
- **View Expenses**: Users can view their logged expenses, filtered by date, category, or month.

### 4. Budget Management
- **Add Budgets**: Users can set budgets for different categories.
- **View Budgets**: Users can view their existing budgets.
- **Update Budgets**: Users can modify their budgets by increasing or decreasing the allocated amount.

### 5. Gamification Features
- Introduced **badges** for user achievements. For example:
  - **Savings Sultan**: Awarded to users who save more than a predefined amount (e.g., $10,000).
  - **Big Spender**: Awarded to users who spend more than $5,000 in a month.

### 6. Security Improvements
- **Password Hashing**: All passwords are securely hashed before being stored in the database.
- **Token Expiry**: Tokens have expiration times to enhance security.

### 7. Enhanced Error Handling
- Improved error messages and responses for invalid requests.

### 8. Performance Optimizations
- Optimized queries for faster expense and budget retrieval.

### 9. Modular Code Structure
- The codebase has been reorganized for better maintainability and scalability. Routes are now modularized into `users`, `expenses`, and `budgets`.

## Features in Version 2

1. **User Authentication**
   - User Registration
   - Secure Login with Token Authentication
   - Password Reset with OTP

2. **Expense Management**
   - Add Expenses
   - View Expenses (filter by date, category, or month)

3. **Budget Management**
   - Add Budgets
   - View Budgets
   - Update Budgets

4. **Gamification**
   - Earn badges for achieving financial goals or demonstrating specific spending/saving habits.

5. **Security Enhancements**
   - Secure password hashing
   - Token-based API security

6. **Database Improvements**
   - PostgreSQL backend for better scalability and performance

## Hidden Features (Easter Eggs)
- Unique achievements and badges for streak-based activities.
- Smart notifications for unusual spending patterns (to be implemented).

---
This version aims to provide a modern, reliable, and user-friendly experience for managing personal finances. Future updates will include more gamification features, predictive analytics, and reward optimizations.
