### User Request Automation - Mobile API & Deployment Guide
This project provides a PHP backend with two API endpoints designed to be used by a mobile application. It allows authorized dealers to update the default layout for a specific display device by automating the process on the Mahindra CMS portal.

## Project Architecture
The project consists of two main PHP scripts that function as API endpoints:

- 1. `get_layouts.php`: A simple API to fetch a list of layouts that a specific dealer is authorized to use.

- 2. `automate.php`: The core automation API that receives display and layout information, then uses Selenium to perform the update on the server.

The project is self-contained; all layout and dealership data is embedded within `get_layouts.php`, removing the need for external data files.

## API Endpoint Documentation
Here is the detailed documentation for the two API endpoints that your mobile application will need to call.

1. Get Shared Layouts
This endpoint provides a list of layout names that are shared with a specific dealership.

2. URL: `https://yourdomain.com/User-Request/get_layouts.php`

3. Method: `GET`

# Query Parameters:

`dealershipCode` (string, required): The dealer's code (e.g., `a012031`). The mobile app should ensure this is sent in lowercase.

# Success Response (`200 OK`):

A JSON array of strings, where each string is a layout name. The list will be alphabetically sorted.

Example Request (from mobile app):
`GET https://yourdomain.com/User-Request/get_layouts.php?dealershipCode=a012031`

1. Assign Layout
This is the main endpoint that triggers the Selenium automation to update a display's layout.

2. URL: `https://yourdomain.com/User-Request/automate.php`

3. Method: `POST`

# Body Parameters (`multipart/form-data`):

`dealershipCode` (string, required): The dealer's code, used for logging into the CMS portal.

`displayName` (string, required): The unique identifier for the display. This should be the serial number extracted from the scanned QR code.

`layout` (string, required): The name of the layout selected by the user from the list provided by the get_layouts.php endpoint.

# Success Response (`200 OK`):

A JSON object indicating success.

# Error Response (`200 OK`):

A JSON object indicating failure, with a descriptive error message.

## Server Deployment Instructions
This guide explains how to deploy the application on a standard Linux server (like a Hostinger VPS, DigitalOcean Droplet, etc.).

# Step 1: Connect to Your Server
First, you need to connect to your server's command line using SSH. You will get the IP address, username, and password from your hosting provider.

```
ssh your_username@your_server_ip
```

# Step 2: Install Dependencies
Your project relies on PHP libraries (from Composer) and server software (Chrome).

1. Install Composer:

```
# Update your server's package list
sudo apt update

# Install composer and other necessary tools
sudo apt install composer git unzip
```

2. Upload Your Project:

Upload your `User-Request` folder (containing `automate.php`, `get_layouts.php`, and `composer.json`) to your server's web root (e.g., `/var/www/html/`). You can use an FTP client like FileZilla or your hosting provider's File Manager.

3. Install PHP Libraries:

Navigate to your project directory in the terminal and run Composer.

```
cd /var/www/html/User-Request
composer install
```

This will download the PHP WebDriver library into a `vendor` folder.

# Step 3: Install Google Chrome on the Server
The server needs its own browser for Selenium to control.

```
# Download the Google Chrome installer
wget [https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb)

# Install Chrome
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Fix any potential dependency issues
sudo apt-get install -f -y
```

# Step 4: Install and Run ChromeDriver on the Server

1. Check Your Chrome Version: You must download a ChromeDriver that exactly matches the version of Chrome you just installed.

```
google-chrome --version
```

2. Download the Correct ChromeDriver:

- Go to the Chrome for Testing availability dashboard using this link: `https://googlechromelabs.github.io/chrome-for-testing/`.

- Find the version that matches your server's Chrome version.

- Copy the download link for the `chromedriver-linux64.zip` file.

- Use `wget` to download it to your server (paste the link you copied).

```
# Example for Chrome 128 - REPLACE THIS URL with the one you copied
wget [https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.84/linux64/chromedriver-linux64.zip](https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.84/linux64/chromedriver-linux64.zip)
```
3. Unzip and Prepare the Driver:

```
# Unzip the file
unzip chromedriver-linux64.zip

# Navigate into the new directory
cd chromedriver-linux64/

# Make the driver executable
chmod +x chromedriver
```
4. Run ChromeDriver as a Background Service:
For the API to work, ChromeDriver must be running constantly. We'll use a tool called `screen` to keep it running in the background.

```
# Install screen
sudo apt install screen

# Start a new, named session for our driver
screen -S chromedriver_session

# You are now inside a virtual terminal. Start the driver.
# This is the Linux equivalent of the command you asked about.
./chromedriver --port=4444

# Now, detach from the session by pressing two key combinations:
# 1. Ctrl+A
# 2. Then press D
```
The terminal will say `[detached]`. Your ChromeDriver is now running silently in the background, and your API is ready to use. If you ever need to view its output again, you can reconnect with `screen -r chromedriver_session`.
