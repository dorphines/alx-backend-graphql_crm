# ALX Travel App 0x02 - Chapa Payment Integration

This project is a Django-based travel booking application with integrated Chapa Payment Gateway.

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd alx_travel_app_0x02
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install Django djangorestframework requests python-dotenv celery psycopg2-binary drf_yasg
    ```

4.  **Database Migrations:**
    ```bash
    python3 manage.py makemigrations listings
    python3 manage.py migrate
    ```

5.  **Create a Superuser (for Admin Panel access):**
    ```bash
    python3 manage.py createsuperuser
    ```

## Chapa API Credentials

1.  **Create a Chapa Account:**
    Go to [https://developer.chapa.co/](https://developer.chapa.co/) and create an account. Obtain your **Secret Key** from your dashboard.

2.  **Set up Environment Variable:**
    Create a `.env` file in the `alx_travel_app_0x02` directory (the same level as `manage.py`) and add your Chapa Secret Key:

    ```
    CHAPA_SECRET_KEY=YOUR_CHAPA_SECRET_KEY
    ```
    **Replace `YOUR_CHAPA_SECRET_KEY` with your actual secret key.**

## Running the Development Server

```bash
python3 manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.

## API Endpoints for Payment

*   **Payment Initiation:**
    *   **Endpoint:** `/api/listings/payment-initiate/`
    *   **Method:** `POST`
    *   **Authentication:** Token-based (requires a logged-in user)
    *   **Request Body Example:**
        ```json
        {
            "booking_id": 1
        }
        ```
    *   **Response:**
        ```json
        {
            "message": "Payment initiated",
            "checkout_url": "https://checkout.chapa.co/checkout/...",
            "payment_id": 1
        }
        ```
    *   **Usage:** After creating a booking (via `/api/bookings/`), use the `booking_id` to initiate payment. The `checkout_url` will redirect the user to Chapa's payment page.

*   **Payment Verification:**
    *   **Endpoint:** `/api/listings/payment-verify/`
    *   **Method:** `GET`
    *   **Usage:** This endpoint is primarily intended as a callback URL for Chapa after a payment is made. You can test it manually by navigating to `http://127.0.0.1:8000/api/listings/payment-verify/?trx_ref=YOUR_TRANSACTION_REF` after a payment attempt. Chapa will redirect users to this URL with `trx_ref` as a query parameter.

## Testing the Payment Workflow

1.  Ensure the development server is running and your `CHAPA_SECRET_KEY` is set in `.env`.
2.  **Create a User:** Register a user or create one via the Django admin panel (`/admin/`).
3.  **Create a Listing:** Create a listing via the Django admin panel or an API endpoint (if you have one).
4.  **Create a Booking:** As the created user, make a POST request to `/api/bookings/` to create a booking for a listing. The response will include the booking details and the Chapa payment initiation details.
5.  **Initiate Payment:** Take the `booking_id` from the booking creation response and make a POST request to `/api/listings/payment-initiate/`.
6.  **Simulate Chapa Checkout:** Copy the `checkout_url` from the initiation response and open it in a browser. Use Chapa's sandbox environment details to complete a test payment.
7.  **Verify Payment:** After completing the payment, Chapa will redirect to your `payment-verify` callback URL. The system should update the payment status. You can check the Django admin panel to see the `Payment` object's status.

## Celery for Email Notifications

The current implementation includes a commented-out line to trigger a Celery task for sending confirmation emails. To enable this:

1.  Set up a Celery worker and a message broker (e.g., Redis or RabbitMQ).
2.  Uncomment the `send_confirmation_email.delay(...)` line in `PaymentVerificationView`.
3.  Implement the `send_confirmation_email` Celery task.

## Swagger/Redoc Documentation

You can access the API documentation at:
*   Swagger UI: `http://127.0.0.1:8000/swagger/`
*   ReDoc: `http://127.0.0.1:8000/redoc/`

Happy coding! ✨
