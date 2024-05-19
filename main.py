import cv2
# To reize image
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

# Read the image file
image = cv2.imread("image.jpg")
# Resize and standardise the image
image = imutils.resize(image, width=500)
# Display original image when it will start finding
cv2.imshow("Original Image", image)
cv2.waitKey(0)
# Convert to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Scale Image", gray)
cv2.waitKey(0)
# Noise reduction
gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("Smoother Image", gray)
cv2.waitKey(0)
# Find edges of images
edged = cv2.Canny(gray, 170, 200)
cv2.imshow("Canny Edge", edged)
cv2.waitKey(0)
# Contours based on the images
cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# Create a copy of original image to draw all contours
image1 = image.copy()
cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
cv2.imshow("Canny after Contouring", image1)
cv2.waitKey(0)
# Reverse the order of sorting
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
NumberPlateCount = None

image2 = image.copy()
cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
cv2.imshow("Top 30 Contours", image2)
cv2.waitKey(0)

# Find the best possible contour
count = 0
name = 1
for i in cnts:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
    if (len(approx) == 4):
        NumberPlateCount = approx
        x, y, w, h = cv2.boundingRect(i)
        crp_img = image[y:y + h, x:x + w]
        cv2.imwrite(str(name) + ".png", crp_img)
        name += 1
        break

cv2.drawContours(image, [NumberPlateCount], -1, (0, 255, 0), 3)
cv2.imshow("Final Image", image)
cv2.waitKey(0)

# Crop only the part of number plate
crop_img_loc = "1.png"
cv2.imshow("Cropped Image", cv2.imread(crop_img_loc))
cv2.waitKey(0)

text = pytesseract.image_to_string(crop_img_loc, lang="eng")
print("Number is = ", text)
cv2.waitKey(0)
