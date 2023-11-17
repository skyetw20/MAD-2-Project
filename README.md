# Project Overview

## Description

This project develops a Ticket Booking Platform, featuring Flask for API, VueJS for dynamic UI, and SQLite for database. Admins create theaters and shows, each with unique attributes, while users book tickets for various movies. Redis aids in caching, while Redis and Celery handle batch jobs. Compatibility extends to Linux and Windows (WSL).

## Technologies Used

- **Flask**: A lightweight web framework for building web applications in Python.
- **Vue.js**: A progressive JavaScript framework for building user interfaces.
- **Bootstrap**: A popular front-end framework for creating responsive and stylish web designs.
- **JWT (JSON Web Tokens)**: A method for securely transmitting information between parties as a JSON object.
- **Redis**: An open-source, in-memory data structure store used for caching and real-time data processing.
- **Celery**: A distributed task queue library for asynchronous processing in Python.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Flask-CORS**: An extension for Flask that simplifies Cross-Origin Resource Sharing (CORS) handling.
- **smtplib**: A module for sending emails using the Simple Mail Transfer Protocol (SMTP).
- **MailHog**: An email testing tool and SMTP server designed for capturing, displaying, and testing email messages sent from applications during development and testing phases.

## DB Schema Design

### Shows
- **Fields**: id, name, rating, tag, duration, ticket_price
- **Primary key**: Shows.id
- Stores information about shows, such as name, rating, tag, duration, and ticket price.

### Theaters
- **Fields**: id, name, place, capacity, capacity_booked, rating
- **Primary key**: Theaters.id
- Stores information about theaters, such as name, place, capacity, capacity_booked, and rating.

### User
- **Fields**: id, name, email, role, password, last_access
- **Primary key**: User.id
- Stores information about users, such as name, email, role, password, and last_access.

### Booking
- **Fields**: id, user_id, show_id, booking_date, booking_time, total_price, num_seats_booked, theater_id
- **Foreign keys**: user_id, show_id, theater_id (linked to User, Shows, and Theaters tables)
- Stores information about bookings.

### ShowTheaterRelation
- **Fields**: id, show_id, theater_id
- **Foreign keys**: show_id, theater_id (linked to Shows and Theaters tables)
- Stores the relationship between shows and theaters.

## API Design

- **/shows (GET)**: Retrieve a list of all available shows.
- **/relation (GET)**: Get relationships between shows and theaters.
- **/theaters (GET)**: Retrieve a list of all available theaters.
- **/login (POST)**: User login using email and password.
- **/logout (GET)**: User logout.
- **/signup (POST)**: User signup with name, email, and password.
- **/account (GET)**: Get user account details by user ID.
- **/bookings (POST)**: Add booking details for a show.
- **/addshow (POST)**: Add details for a new show.
- **/addtheater (POST)**: Add details for a new theater.
- **/updateshow (PUT)**: Update details of an existing show.
- **/updatetheater (PUT)**: Update details of an existing theater.
- **/deleteshow (DELETE)**: Delete a show by email and show ID.
- **/deletetheater (DELETE)**: Delete a theater by email and theater ID.
- **/exporttheater (POST)**: Export details of a theater.
- **/test (GET)**: Test the API functionality.

## Architecture and Features

The architecture of the project is thoughtfully divided into two pivotal components: the frontend and the backend. The backend orchestrates the core functionality using Flask, a versatile framework that seamlessly constructs a robust REST API. This API serves as the backbone for user interaction, seamlessly facilitating user authentication through the utilization of JWT tokens. The backend further enhances performance by incorporating Redis, a high-performance caching solution. By storing frequently accessed data in Redis, the app significantly reduces the load on the database, resulting in quicker response times and a smoother user experience. Moreover, the integration of Celery introduces a layer of asynchronous capabilities to the backend. This enables the system to efficiently manage tasks that don't need to be executed immediately, such as sending email alerts, generating detailed reports, and orchestrating data exports. This strategic implementation of Celery ensures that these resource-intensive operations don't disrupt the app's responsiveness and overall performance.

On the frontend, the Vue.js framework is used to create an intuitive and engaging user interface. Within the "src" directory, the carefully organized "components" folder houses modular components that encapsulate specific functionalities, enhancing maintainability and reusability. Core configuration files, including the router and "main.js," are strategically placed within the "src" directory, facilitating a seamless entry point for the frontend. This well-structured architecture culminates in a cohesive single-page application that seamlessly communicates with the backend through the Axios module. To optimize data retrieval and minimize redundant requests, the app employs local storage to efficiently store fetched information. Beyond the foundational features of user authentication and caching, the app offers advanced functionalities that are efficiently managed through Celery. These include the timely dispatch of email notifications, dynamic report generation, and flexible data export capabilities. The integration of Redis and Vue.js, along with the strategic use of Celery, collectively contributes to the project's ability to deliver a responsive, feature-rich, and highly efficient web application.

## Video

[Project Overview Video](https://drive.google.com/file/d/1bHR71HRMDGvp54jo_YVCLwqUVTcrUWSz/view?usp=drive_link)
