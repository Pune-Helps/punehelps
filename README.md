# PuneSeva

**A community-driven platform for requesting and offering help in Pune.**


## About

PuneSeva is an online, single-page application built to foster community support in Pune. Users can post requests for help—ranging from errands and tutoring to pet care—while volunteers (“helpers”) can browse and offer assistance. The project is inspired by and based on the [PuneHelps](https://github.com/Pune-Helps/punehelps) repository.

## Features

- **Request Help**: Registered users can submit detailed help requests via a form.
- **Offer Assistance**: Helpers can browse active requests and volunteer to help.
- **Dynamic Cards**: Requests and offers are displayed as interactive cards.
- **Real-Time Updates**: New requests and helper responses appear without page reload (using AJAX/Fetch API).
- **Authentication**: Secure signup/login system with session management (PHP & MySQL).
- **Responsive Design**: Mobile-friendly layout ensures accessibility on all devices.

## Demo

![Homepage Screenshot](docs/images/homepage.png)

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6), 
- **Backend**: PHP 7+, MySQL
- **Server**: XAMPP (Apache)


## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

- PHP 7.4+ installed
- MySQL server (or MariaDB)
- XAMPP (recommended) or LAMP stack
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Pune-Helps/punehelps.git puneseva
   cd puneseva
   ```

2. **Setup database**
   - Open phpMyAdmin (usually at `http://localhost/phpmyadmin`).
   - Create a database named `puneseva`.
   - Import `database.sql` to create necessary tables.

3. **Configure environment**
   - Rename `config.sample.php` to `config.php`.
   - Update database credentials in `config.php`.

### Configuration

```php
// config.php
<?php
return [
    'db_host' => 'localhost',
    'db_name' => 'puneseva',
    'db_user' => 'root',
    'db_pass' => '',
];
```

### Running the App

1. Start Apache and MySQL via XAMPP control panel.
2. Navigate to `http://localhost/puneseva` in your browser.

## Usage

1. **Sign Up / Log In**: Create an account or log in.
2. **Post Request**: Fill out the "Request Help" form with title, description, urgency, and contact details.
3. **Browse Requests**: Switch to "Help Others" tab to view open requests.
4. **Volunteer**: Click "Help" on a card to volunteer; the requester receives an email notification.
5. **Manage Requests**: Requesters can mark tasks as "Completed" when help is received.



