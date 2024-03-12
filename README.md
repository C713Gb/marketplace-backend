# MarketPlace

MarketPlace is a FastAPI application designed to connect farmers (sellers) and consumers (buyers) in a streamlined platform, enabling sellers to list their produce and buyers to purchase them efficiently.

## Features

- User management system for buyers and sellers
- Product listing, including creation, update, and deletion of product entries
- Transaction processing for purchases
- Real-time updates and notifications
- Secure authentication and authorization

## Technology Stack

- **Backend**: Python, FastAPI
- **Database**: MongoDB
- **Authentication**: JWT for secure authentication
- **Frontend**: (If applicable, mention technologies like Flutter, React)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7+
- MongoDB
- pip

### Installation

1. Clone the repository:
   ```
   git clone https://yourrepository.com/marketplace.git
   ```
2. Navigate to the project directory:
   ```
   cd marketplace
   ```
3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

### Testing

To run the automated tests for this system, execute:

```
pytest
```

## API Documentation

Once the server is running, you can access the Swagger UI to test the API endpoints at:

```
http://127.0.0.1:8000/docs
```

## Authors

- **Gourav Banerjee** - [GitHub](https://github.com/C713Gb)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
