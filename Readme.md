# Image Processor and Email Sender

## Overview
The Image Processor and Email Sender is a Python application built using the Tkinter library. It allows users to select folders containing images, process those images (apply aesthetic filters or convert them to greyscale), and send the processed images via email using a specified Gmail account.

## Features
- *GUI Interface*: User-friendly interface for selecting folders and inputting Gmail credentials.
- *Image Processing*: Apply aesthetic filters or convert images to greyscale.
- *Email Sending*: Send processed images via email using a Gmail account.
- *Folder Monitoring*: Continuously monitor specified folders for new images and process them automatically.
- *Multi-threading*: Uses threading to monitor folders and process images without freezing the GUI.
- *Queue System*: Updates the GUI with status messages using a queue system.

## Requirements
- Python 3.x
- Tkinter
- Pillow
- smtplib
- queue

## Installation
1. Ensure you have Python 3.x installed on your system.
2. Install the required libraries using pip:
    bash
    pip install tkinter pillow
    

## Usage
1. Run the script:
    bash
    python asthetic.py
    
2. Use the GUI to:
    - Select the folder for aesthetic image processing.
    - Select the folder for greyscale image processing.
    - Enter the Gmail ID for sending emails.
3. Click the "Start Monitoring" button to begin monitoring the selected folders for new images.
4. The application will process any new images in the selected folders and send them to the specified Gmail account.

## File Structure
- *asthetic.py*: Main script containing the application logic and GUI.

## Application Workflow
1. *Initialization*: Sets up the GUI and initializes variables.
2. *Creating Widgets*: Configures the styles and places the widgets on the GUI.
3. *Image Processing*: Applies the specified filter to the images.
4. *Sending Email*: Uses the smtplib library to send processed images via email.
5. *Folder Monitoring*: Continuously checks the specified folders for new images and processes them.

## Error Handling
- The application displays error messages in a message box for issues like missing Gmail ID.
- The status bar updates with error messages if email sending fails.

## Notes
- Ensure that the selected folders contain images with extensions .png, .jpg, or .jpeg.
- The Gmail account used for sending emails must have "Less secure app access" enabled.

## Author
- Jupalli Prabhas
