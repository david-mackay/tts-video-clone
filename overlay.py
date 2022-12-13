def overlay_text_on_video(input_video, string):

    # Import the necessary packages
    import cv2
    import numpy as np

    # Load the input video
    video = cv2.VideoCapture(input_video)

    # Check if the video was successfully loaded
    if not video.isOpened():
        print("Error opening video file")
        return

    # Read the first frame from the video
    success, frame = video.read()

    # Check if the frame was successfully read
    if not success:
        print("Error reading first frame from video")
        return

    # Calculate the duration of each sentence
    words = string.split(".")
    duration = len(words) / 200 # 200 words per minute

    # Create a black image with the same size as the frame
    image = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

    # Get the size of the string and set the font
    size, _ = cv2.getTextSize(string, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Loop through the video frames
    while True:
    # Read the next frame from the video
        success, frame = video.read()

        # If the frame was not successfully read, break the loop
        if not success:
            break

        # Put the string on the image
        cv2.putText(image, string, (int((frame.shape[1]-size[0])/2), int((frame.shape[0]+size[1])/2)), font, 1, (255,255,255), 2, cv2.LINE_AA)

        # Overlay the image on the frame
        frame = cv2.addWeighted(frame, 1, image, 1, 0)

        # Display the frame
        cv2.imshow("Frame", frame)

        # Wait for the duration of the sentence
        key = cv2.waitKey(int(duration*1000))

        # If the user presses 'q', break the loop
        if key == ord('q'):
            break
    # Release the video and destroy all windows
    video.release()
    cv2.destroyAllWindows()

    # Example usage
    overlay_text_on_video("input_video.mp4", "This is a sentence.")

def overlay_text_on_video2(input_video, string):
  # Import the necessary packages
  import cv2
  import numpy as np

  # Load the input video
  video = cv2.VideoCapture(input_video)

  # Check if the video was successfully loaded
  if not video.isOpened():
    print("Error opening video file")
    return

  # Read the first frame from the video
  success, frame = video.read()

  # Check if the frame was successfully read
  if not success:
    print("Error reading first frame from video")
    return

  # Create a black image with the same size as the frame
  image = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

  # Get the size of the string and set the font
  size, _ = cv2.getTextSize(string, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
  font = cv2.FONT_HERSHEY_SIMPLEX

  # Loop through the video frames
  while True:
    # Read the next frame from the video
    success, frame = video.read()

    # If the frame was not successfully read, break the loop
    if not success:
      break

    # Put the string on the image
    cv2.putText(image, string, (int((frame.shape[1]-size[0])/2), int((frame.shape[0]+size[1])/2)), font, 1, (255,255,255), 2, cv2.LINE_AA)

    # Overlay the image on the frame
    frame = cv2.addWeighted(frame, 1, image, 1, 0)

    # Display the frame
    cv2.imshow("Frame", frame)

    # Wait for 1ms
    key = cv2.waitKey(1)

    # If the user presses 'q', break the loop
    if key == ord('q'):
      break

  # Release the video and destroy all windows
  video.release()
  cv2.destroyAllWindows()

overlay_text_on_video2("sampleparkour.webm", "This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test.")
