# Modern Banking System

A modern banking system with a graphical user interface built using Python and Tkinter. This project implements a complete banking solution with user authentication, account management, and transaction processing.

## Features

- User Authentication
  - User registration with secure password hashing
  - Login system with customer ID and password
  - Session management

- Account Management
  - Create new bank accounts
  - View account balances
  - Transaction history tracking
  - Account balance search using BST

- Banking Operations
  - Cash deposits
  - Cash withdrawals
  - Money transfers between accounts
  - Priority transaction processing for large amounts

- Data Structures
  - HashMap for efficient data storage
  - LinkedQueue for transaction history
  - MaxHeap for priority transactions
  - Balanced BST for account balance search

## Technical Details

### Data Structures
- **HashMap**: Custom implementation for storing customers and accounts
- **LinkedQueue**: Custom queue implementation for transaction history
- **MaxHeap**: Priority queue for handling large transactions
- **BalanceBST**: Binary search tree for efficient balance range queries

### Security Features
- Password hashing using SHA-256
- Input validation
- Access control for account operations

### Data Persistence
- JSON-based data storage
- Automatic data saving after each operation
- Transaction history tracking


## Requirements

- Python 3.x
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Navigate to the project directory:
```bash
cd banking_project
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **Registration**
   - Click "Register" on the welcome screen
   - Enter your name and password
   - Save your customer ID for future logins

2. **Login**
   - Enter your customer ID and password
   - Click "Login"

3. **Account Operations**
   - Create new accounts
   - Perform deposits and withdrawals
   - Transfer money between accounts
   - View transaction history

## Security Notes

- Passwords are hashed using SHA-256
- Minimum password requirements:
  - At least 8 characters
  - Must contain letters and numbers
- All transactions are logged with timestamps

## Error Handling

The system includes comprehensive error handling for:
- Invalid login attempts
- Insufficient funds
- Invalid transaction amounts
- Unauthorized access attempts
- Data validation errors

## Future Improvements

- Multi-language support
- Enhanced security features
- Mobile application
- Web interface
- API integration
- Real-time transaction notifications
- Advanced reporting features

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python and Tkinter
- Uses custom data structures for optimal performance
- Implements modern banking practices and security measures
