# Song Leading

Builds a song list and emails it out.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Overview
This project automates the process of creating a song list and distributing it via email. It is designed to streamline workflows for song leaders, music directors, or anyone managing song selections for events.

## Features
- Create and manage song lists.
- Automatically format song lists for email distribution.
- Send emails directly from the application.
- Customizable templates for song lists and email content.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/song-leading.git
   ```
2. Navigate to the project directory:
   ```bash
   cd song-leading
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Configure the application (see [Configuration](#configuration)).
2. Run the script to generate and send the song list:
   ```bash
   python main.py
   ```
3. Follow the prompts to input song details or use a predefined list.

## Configuration
To set up the application, you need to configure email settings and other parameters:

1. Create a `.env` file in the project root to store sensitive information like email credentials.
2. Example `.env` file:
   ```env
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_USER=your-email@example.com
   EMAIL_PASSWORD=your-email-password
   ```
3. Customize templates or settings in the `config/` directory if applicable.

## Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push the branch:
   ```bash
   git commit -m "Add feature-name"
   git push origin feature-name
   ```
4. Open a pull request and provide a detailed description of your changes.

## License
This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this project as long as the license terms are followed.

---

Feel free to reach out if you have any questions or suggestions for improvement!
