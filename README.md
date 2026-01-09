# ALX Backend GraphQL CRM

This project is a Customer Relationship Management (CRM) system built with Django and GraphQL. It provides a GraphQL API to manage customers, products, and orders.

## Project Structure

- `crm/`: The Django app that contains the core CRM logic.
- `settings.py`: The Django settings file.
- `urls.py`: The Django URL configuration.
- `wsgi.py`: The WSGI configuration.
- `schema.py`: The main GraphQL schema.
- `manage.py`: The Django management script.
- `db.sqlite3`: The SQLite database file.

## Features

- **GraphQL API**: A single endpoint (`/graphql`) for all data operations.
- **CRUD Operations**: Create, read, update, and delete customers, products, and orders.
- **Bulk Operations**: Bulk create customers.
- **Filtering**: Filter customers, products, and orders based on various criteria.
- **Pagination**: Paginate through large datasets.
- **Sorting**: Sort query results.

## Models

### Customer

- `name`: `CharField`
- `email`: `EmailField` (unique)
- `phone`: `CharField`
- `created_at`: `DateTimeField`

### Product

- `name`: `CharField`
- `price`: `DecimalField`
- `stock`: `PositiveIntegerField`

### Order

- `customer`: `ForeignKey` to `Customer`
- `products`: `ManyToManyField` to `Product`
- `order_date`: `DateTimeField`
- `total_amount`: `DecimalField`

## GraphQL Schema

### Types

- `CustomerType`: Represents a customer.
- `ProductType`: Represents a product.
- `OrderType`: Represents an order.

### Queries

- `allCustomers`: Returns a paginated list of customers.
  - `filter`: Filter by `name`, `email`, `created_at`, and `phone_pattern`.
  - `orderBy`: Sort by any field.
- `allProducts`: Returns a paginated list of products.
  - `filter`: Filter by `name`, `price`, `stock`, and `low_stock`.
  - `orderBy`: Sort by any field.
- `allOrders`: Returns a paginated list of orders.
  - `filter`: Filter by `total_amount`, `order_date`, `customer_name`, `product_name`, and `product_id`.
  - `orderBy`: Sort by any field.

### Mutations

- `createCustomer`: Creates a new customer.
- `bulkCreateCustomers`: Creates multiple customers in a single request.
- `createProduct`: Creates a new product.
- `createOrder`: Creates a new order.

## Running the Project

1.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    *Note: A `requirements.txt` file would need to be generated first.*

2.  **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

3.  **Run the development server**:

    ```bash
    python manage.py runserver
    ```

4.  **Access the GraphiQL interface**:

    Open your browser and navigate to `http://127.0.0.1:8000/graphql`.

## Example Queries and Mutations

### Create a Customer

```graphql
mutation {
  createCustomer(input: {
    name: "John Doe",
    email: "john.doe@example.com",
    phone: "+11234567890"
  }) {
    customer {
      id
      name
      email
    }
    message
  }
}
```

### Filter Products

```graphql
query {
  allProducts(filter: { priceGte: 100, priceLte: 500 }, orderBy: "-stock") {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```
