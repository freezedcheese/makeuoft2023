# MakeUofT2023

## Inspiration
As some of our team members have little siblings, we understand the struggle of living with them! So, now that we're in university, we've grown to miss all of their little quirks. So, why not bring them back?

## What it does
Our robot searches for people, and once found, will track them and move toward them. When it gets close enough, our robot will spray you with water, before giggling and running away. Ahhhh, feels JUST like home!

## How we built it
We connected an iPhone via Bluetooth to a computer, where we analyze the footage in Python. Using the OpenCV library, our program finds a person and calculates where they are relative to the frame. The laptop then tells an Arduino over Bluetooth where the person is, and the Arduino then changes the velocity of two motors to control the speed and direction of the robot, ensuring that it meets its subject at an optimal distance for spraying. The enclosure is built from a combination of cardboard, 3D-printed supports, and screws.


## Challenges we ran into
Integrating all of the components together proved to be a challenge. While they seemed to work on their own, communicating between each piece was tricky. For example, we were all relatively new to asynchronous programming, so designing a Python script to both analyze footage and send the results over Bluetooth to the Arduino was more difficult than anticipated.

## Accomplishments that we're proud of

It works! Based on what the camera sees, our motors change direction to put the robot on a perfect spray trajectory!

## What we learned

We improved our programming skills, learned how to communicate between devices over Bluetooth, and operate the Arduino. We were able to use a camera and understand the position of a person using computer vision.

## What's next for Your Annoying Little Sibling

We would love to further improve our robot's tracking skills and incorporate more sibling-like annoyances like slapping, biting, and telling tattle tales.
