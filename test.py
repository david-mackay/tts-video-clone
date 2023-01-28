import cv2
import numpy as np
def create_typing_video(text, output_filename, width=640, height=480, font_scale=2, font_color=(0, 255, 0)):
    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(output_filename, fourcc, 30.0, (width, height))

    # Create an image with a black background
    img = np.zeros((height, width, 3), np.uint8)

    # Set the font and draw the text on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (10, 50), font, font_scale, font_color, 2, cv2.LINE_AA)

    # Split the text into individual characters
    chars = list(text)

    # Set the initial x coordinate
    x = 10

    # Iterate through the characters and create a video frame for each character
    for c in chars:
        # Get the size of the character
        (w, h), baseline = cv2.getTextSize(c, font, font_scale, 2)

        # Set the y coordinate
        y = 50 - h

        # Draw the character on the image
        # cv2.rectangle(img, (x,y), (x+w, y+h), font_color, -1)
        cv2.putText(img, c, (x, y-10), font, font_scale, (0, 0, 0), 2, cv2.LINE_AA)

        # Add the image to the video writer
        out.write(img)

        # Increment the x coordinate
        x += w

    # Release the video writer
    out.release()

# Test the function
text = "This is a test of the typing video function."
create_typing_video(text, "typing_video.mp4")
