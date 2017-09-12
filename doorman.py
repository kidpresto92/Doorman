# This project was original to be used from a raspberry pi to
# caputre an image using a webcam and send it to your phone 
# using the email address of your service provider 
# ex) ###-###-####@vzwpix.com 

import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

### Constants
# Local path of the directory where the image will be saved
IMAGE_DIRECTORY = "C:/Users/aaron/Projects/python/doorman/"

# The file name of the image that we'll capture
IMAGE_FILENAME = "image.png"

# Used to separate RECIPIENTS
COMMASPACE = ", "

# Gmail Account used to send the Email
GMAIL_ACCOUNT = "fakeEmail@gmail.com"

# Password of the above Gmail Account
GMAIL_PASSWORD = "fakePassword"

# The SMTP server used to send an email from a gmail account
GMAIL_SMTP_SERVER = "smtp.gmail.com:587"

# message to be used in the body of the email
MESSAGE_TEXT = "You have a visitor!"

# message to be used in the body of the email
MESSAGE_SUBJECT = "Test"

# message to be used in the body of the email
MESSAGE_FROM = "Your Front Door"


# List of all email accounts that will receive the image
RECIPIENTS = ['fakeRecipient@gmail.com'] # my cell phone number

# The first available camera
cap = cv2.VideoCapture(0)

#captures an image using the webcam (or capture device: cap)
def GetImage():
    retval, image = cap.read()
    return image
   

pictureTaken = GetImage()

# Save the file to a local directory
cv2.imwrite(IMAGE_DIRECTORY + IMAGE_FILENAME, pictureTaken)
    
try:
    # Message composition
    msg = MIMEMultipart()
    msg['From'] = MESSAGE_FROM
    msg['To'] = COMMASPACE.join(RECIPIENTS)
    msg['Subject'] = (MESSAGE_SUBJECT)
    msg.attach(MIMEText(MESSAGE_TEXT))

    # Finding the picture in the directory and adding it to the message
    fp = open(IMAGE_DIRECTORY + IMAGE_FILENAME, 'rb')
    img = MIMEImage(fp.read())
    msg.attach(img)
    fp.close()
    
    # Open the SMTP connection and send the email
    server = smtplib.SMTP(GMAIL_SMTP_SERVER)
    server.ehlo()
    server.starttls()
    server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
    server.sendmail(GMAIL_ACCOUNT, RECIPIENTS, msg.as_string())
    server.quit()
    
    print "Successfully Sent"
    
except Exception as ex:    
    print "Error Sending"
    print(ex)
    
cap.release()