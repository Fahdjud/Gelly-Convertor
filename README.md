![Fahdjud Auction Platform](Banner.webp)

# Gilly Converter

#### Description:
Gilly Converter is a powerful tool built with Flask that quickly converts PNG files to WebP format.

#### Features:
- Fast and efficient conversion
- User-friendly interface
- Batch processing support
- High-quality output

#### Pages:
- **Home Page**: Upload PNG files and convert them to WebP.
- **Login Page**: Access additional features by logging in.
- **Register Page**: Create a new account to start using the app.

#### Authentication:
- **Login**: Log in with your email and password.
- **Register**: Sign up with your email, username, and password.
- **Logout**: Securely log out of your account.

#### Usage:
1. Start the Flask application:
    ```bash
    flask run
    ```
2. Open your browser and go to `http://127.0.0.1:5000`
3. Upload your PNG files and click convert

#### Database:
- **SQLite**: Stores user information securely.
- **User Data**: Credentials and session info are stored in the database.
- **SQLAlchemy**: Used as the ORM to interact with the SQLite database.

#### Credits:
- **Credit System**: Manages the usage of the conversion feature. Users get a certain number of credits upon registration.
- **Using Credits**: Each conversion deducts credits from the user's account. Ensure you have enough credits for conversions.

#### Error Handling:
- **Graceful Error Messages**: Provides user-friendly error messages for common issues.
- **Logging**: Logs errors and important events for debugging and monitoring.

#### Security:
- **Password Hashing**: Passwords are hashed securely before storage.
- **Input Validation**: Validates user inputs to prevent security vulnerabilities.
- **HTTPS**: Supports HTTPS for secure communication.

#### Future Enhancements:
- **Additional File Formats**: Support for mov, webm.
- **Advanced Settings**: Options to customize conversion settings.

#### Installation:
1. Navigate to the project directory:
    ```bash
    cd gilly-converter
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up the environment variables:
    ```bash
    cp .env.example .env
    ```
4. Initialize the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

    #### Jilly Theme:
    The Jilly theme is a custom Bootstrap theme crafted to give the Gilly Converter application a sleek and modern appearance. It significantly enhances the user experience by providing a responsive and visually appealing interface.

    #### Bootstrap Integration:
    - **Responsive Design**: Leveraged Bootstrap's grid system to ensure the application is fully responsive and functions seamlessly across various devices.
    - **Custom Styling**: Tailored Bootstrap components such as buttons, forms, and navigation bars to align with the Jilly theme's aesthetic.
    - **Consistency**: Maintained a consistent look and feel across all pages by utilizing Bootstrap's utility classes and components.
    - **Ease of Use**: Streamlined the development process by using Bootstrap's pre-built components, enabling rapid prototyping and implementation.

    By integrating Bootstrap, the Gilly Converter application not only looks professional but also offers a smooth and intuitive user experience.