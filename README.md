## Security camera system leveraging the Google Vision AI API

This diagram illustrates the workflow of this system.

![Untitled drawing](https://github.com/andyelu/ai-closet-security-cam/assets/126619706/f845beed-502b-49c9-a1c4-b7d2b5224e16)

Trigger: The system activates when the Arduino light sensor in the closet detects light.

Signal Transmission: Upon activation, the Arduino sends a serial message to the Raspberry Pi.

HTTP Request: The Raspberry Pi, connected to WiFi, sends an HTTP request to the Django Webserver.

Image Retrieval: The Django Webserver executes a Python script to send a GET request to the camera for the current frame.

Object Detection: This image is processed through the Google Cloud Vision AI API to identify if a human is present.

Storage and Logging: If a human is detected by the Vision AI, the image is stored in an Amazon S3 bucket and recorded in an SQLite database.

Notification: When that happens, an email with the image URL is sent to the user.
