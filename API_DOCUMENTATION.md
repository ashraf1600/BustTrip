# BusTrip Backend API Documentation

## Base URL

Example base URL:

- `http://<host>:<port>/api/`

---

## Authentication

This backend uses token-based authentication via Django REST Framework's `TokenAuthentication`.

### Register a new user

- Endpoint: `POST /api/register/`
- Description: Create a new user account and return an auth token.
- Request body:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword"
  }
  ```
- Response (201 Created):
  ```json
  {
    "token": "<user-auth-token>"
  }
  ```
- Response (400 Bad Request): validation errors.

### Login an existing user

- Endpoint: `POST /api/login/`
- Description: Authenticate with username and password and return a token.
- Request body:
  ```json
  {
    "username": "johndoe",
    "password": "securepassword"
  }
  ```
- Response (200 OK):
  ```json
  {
    "token": "<user-auth-token>",
    "user_id": 1
  }
  ```
- Response (401 Unauthorized): invalid credentials.

> Note: Use the returned token in the `Authorization` header for protected endpoints.
>
> Example header:
> `Authorization: Token <user-auth-token>`

---

## Bus Endpoints

These endpoints allow clients to list and create buses.

### List all buses

- Endpoint: `GET /api/buses/`
- Description: Retrieve a list of all buses.
- Authorization: Not required.
- Response (200 OK):
  ```json
  [
    {
      "id": 1,
      "bus_name": "Express Line",
      "number": "BUS-101",
      "origin": "City A",
      "destination": "City B",
      "features": "WiFi, AC, Recliner",
      "start_time": "2026-04-27T08:00:00Z",
      "reach_time": "2026-04-27T12:00:00Z",
      "no_of_seats": 40,
      "price": "25.00"
    }
  ]
  ```

### Create a new bus

- Endpoint: `POST /api/buses/`
- Description: Create a new bus record.
- Authorization: Not required.
- Request body:
  ```json
  {
    "bus_name": "Express Line",
    "number": "BUS-101",
    "origin": "City A",
    "destination": "City B",
    "features": "WiFi, AC, Recliner",
    "start_time": "2026-04-27T08:00:00Z",
    "reach_time": "2026-04-27T12:00:00Z",
    "no_of_seats": 40,
    "price": "25.00"
  }
  ```
- Response (201 Created): created bus object.
- Response (400 Bad Request): validation errors.

### Retrieve, update, or delete a bus

- Endpoint: `GET /api/buses/<bus_id>/`
- Endpoint: `PUT /api/buses/<bus_id>/`
- Endpoint: `PATCH /api/buses/<bus_id>/`
- Endpoint: `DELETE /api/buses/<bus_id>/`
- Description:
  - `GET` retrieves bus details.
  - `PUT` or `PATCH` updates bus information.
  - `DELETE` removes the bus.
- Authorization: Not required.

Example `GET` response (200 OK):

```json
{
  "id": 1,
  "bus_name": "Express Line",
  "number": "BUS-101",
  "origin": "City A",
  "destination": "City B",
  "features": "WiFi, AC, Recliner",
  "start_time": "2026-04-27T08:00:00Z",
  "reach_time": "2026-04-27T12:00:00Z",
  "no_of_seats": 40,
  "price": "25.00"
}
```

---

## Booking Endpoints

### Book a seat

- Endpoint: `POST /api/bookings/`
- Description: Create a booking for a seat on a bus.
- Authorization: Required.
- Required header:
  - `Authorization: Token <user-auth-token>`
- Request body:
  ```json
  {
    "seat": 10
  }
  ```

  - `seat` is the ID of the `Seats` record to book.
- Responses:
  - `201 Created`: booking created successfully.
  - `400 Bad Request`: seat is already booked or invalid input.
  - `404 Not Found`: seat ID does not exist.

Example response (201 Created):

```json
{
  "id": 5,
  "user": "johndoe",
  "bus": "Express Line BUS-101 from City A to City B",
  "seat": {
    "id": 10,
    "seat_number": "A1",
    "is_booked": true
  },
  "booking_time": "2026-04-27T09:15:00Z"
}
```

### List bookings for a user

- Endpoint: `GET /api/user/<user_id>/bookings`
- Description: Return all bookings for the specified user.
- Authorization: Required.
- Required header:
  - `Authorization: Token <user-auth-token>`
- Notes:
  - The authenticated user must match the `user_id` in the URL.
  - If the logged-in user ID does not match, response is `401 Unauthorized`.

Example response (200 OK):

```json
[
  {
    "id": 5,
    "user": "johndoe",
    "bus": "Express Line BUS-101 from City A to City B",
    "seat": {
      "id": 10,
      "seat_number": "A1",
      "is_booked": true
    },
    "booking_time": "2026-04-27T09:15:00Z"
  }
]
```

---

## Models

### Bus

Fields:

- `id` (integer)
- `bus_name` (string)
- `number` (string)
- `origin` (string)
- `destination` (string)
- `features` (string)
- `start_time` (datetime)
- `reach_time` (datetime)
- `no_of_seats` (integer)
- `price` (decimal)

### Seats

Fields:

- `id` (integer)
- `bus` (foreign key to `Bus`)
- `seat_number` (string)
- `is_booked` (boolean)

### Booking

Fields:

- `id` (integer)
- `user` (foreign key to Django `User`)
- `bus` (foreign key to `Bus`)
- `seat` (foreign key to `Seats`)
- `booking_time` (datetime, auto-generated)

---

## Notes

- `POST /api/bookings/` expects a valid seat ID and sets `Seats.is_booked` to `true` when the seat is successfully booked.
- Users must authenticate before using protected endpoints (`/api/bookings/`, `/api/user/<user_id>/bookings`).
- The token returned by `/api/register/` and `/api/login/` should be included in the `Authorization` header.

---

## Example Authentication Header

```
Authorization: Token 71f0d4c8dd1b4b1a4f8f159d3b7c2f8e5cc9b841
```
