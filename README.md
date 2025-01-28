# Personal Finance Manager (PFM) Version-2

## Overview
Personal Finance Manager v2 is the successor to the original Personal Finance Manager project. This new version introduces major improvements and additional features aimed at providing a more secure, user-friendly, and robust system for managing personal finances. 

## Major Changes in v2

### 1. Database Migration to PostgreSQL
- The database has been migrated from SQLite to PostgreSQL, providing better performance, scalability, and support for advanced queries.

### 2. User Management
- **User Accounts**: Users can now create their own accounts with a unique user ID and password.
- **Login System**: Users can securely log in to their accounts.
<br></br>
![User Login Demo](https://github.com/user-attachments/assets/dceffc1d-ff8f-46a1-bf4b-bae04f9c0f26)
- **Token-Based Authentication**: All API requests are secured using token-based authentication.
- **Password Reset with OTP**: Users can reset their passwords by verifying their identity through an OTP sent to their registered email.

### 3. Expense Management
- **Add Expenses**: Users can log their expenses by providing details such as category, amount, and date.
<br></br>
![Add Expense Demo](https://github.com/user-attachments/assets/ad1f17cd-247a-4ae6-9c3e-0f467a411f77)
- **View Expenses**: Users can view their logged expenses, filtered by date, category, or month.
<br></br>
![View Expenses Demo](https://github.com/user-attachments/assets/4624aa60-fa64-498f-a161-feb23a9589e3)

### 4. Budget Management
- **Add Budgets**: Users can set budgets for different categories.
<br></br>
![Add Budget Demo](https://github.com/user-attachments/assets/028d884d-3a0c-4474-8563-3601aa20aeb7)
- **View Budgets**: Users can view their existing budgets.
<br></br>
![View Budgets](https://github.com/user-attachments/assets/5abb0b1d-0c6a-4440-886d-0b78addc1688)
- **Update Budgets**: Users can modify their budgets by increasing or decreasing the allocated amount.
<br></br>
![Update Budget Demo](https://github.com/user-attachments/assets/5a61494c-85fa-4860-99c9-da96e21ac992)

### 5. Personalized Dashboard
- Created personalized dashboard for user's to view there financial data.
<br></br>
![Dashboard Demo](https://github.com/user-attachments/assets/f657b885-1ddf-4f0b-a258-7c7506d24f86)

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
