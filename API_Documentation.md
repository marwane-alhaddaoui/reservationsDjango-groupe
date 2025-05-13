# API Documentation

## Overview
This document provides an overview of the API endpoints available in the `reservations` project. The API is built using Django REST Framework and supports features like authentication, user management, cart management, and more.

---

## Authentication

### Endpoints
- **Login**: `/accounts/api/login/`
  - Authenticate a user and obtain a token.
- **Logout**: `/accounts/api/logout/`
  - Terminate the user's session.
- **Check Authentication**: `/accounts/api/auth/check/`
  - Verify if the user is authenticated.

### Authentication Methods
- Token-based authentication (`TokenAuthentication`)
- Session-based authentication (`SessionAuthentication`)

---

## User Management

### Endpoints
- **Sign Up**: `/accounts/signup/`
  - Register a new user.
- **Profile**: `/accounts/profile/`
  - View and update the user's profile.
- **Update Profile**: `/accounts/profile/<int:pk>/`
  - Update a specific user's profile.
- **Delete User**: `/accounts/profile/delete/<int:pk>/`
  - Delete a specific user.

---

## Cart Management

### Endpoints
- **Get Cart**: `/accounts/api/user-cart/<int:user_id>/`
  - Retrieve the user's cart.
- **Update Cart**: `/accounts/api/user-cart/update/`
  - Update items in the cart.
- **Delete Cart Item**: `/accounts/api/user-cart/delete/<int:user_id>/`
  - Remove items from the cart.

---

## Catalogue

### Endpoints
- **Main Catalogue**: `/catalogue/`
  - Access the main catalogue.
- **Artists**: `/catalogue/api/artist/`
  - List and create artists.
- **Artist Details**: `/catalogue/api/artist/<int:pk>/`
  - Retrieve, update, or delete a specific artist.
- **Shows**: `/catalogue/api/show/`
  - List and create shows.
- **Show Details**: `/catalogue/api/show/<int:pk>/`
  - Retrieve, update, or delete a specific show.

---

## Stripe Integration

### Endpoints
- **Create Stripe Session**: `/catalogue/api/stripe/create-session/`
  - Create a Stripe session for payment.

---

## Reviews

### Endpoints
- **List Reviews**: `/catalogue/api/review/`
  - List and create reviews for shows.
- **Review Details**: `/catalogue/api/review/<int:pk>/`
  - Retrieve, update, or delete a specific review.

---

## Other Features

### Endpoints
- **Representations**: `/catalogue/api/representation/`
  - List representations of shows.
- **Prices**: `/catalogue/api/price/`
  - Retrieve price details.

---

## How to Use the API

### Authentication
1. Obtain a token by logging in at `/accounts/api/login/`.
2. Include the token in the `Authorization` header for subsequent requests:
   ```
   Authorization: Token <your-token>
   ```

### Accessing Endpoints
- Use the browsable API by navigating to the endpoint URLs in your browser.
- Alternatively, use tools like Postman or cURL to interact with the API.

### Data Format
- The API accepts and returns data in JSON format.

### Error Handling
- The API returns appropriate HTTP status codes and error messages for invalid requests.
