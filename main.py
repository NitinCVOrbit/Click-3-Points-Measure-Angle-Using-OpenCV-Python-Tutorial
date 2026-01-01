import cv2
import numpy as np

points = []
img = cv2.imread("angle_03.jpg")
img = cv2.resize(img,(1280,720))
img_copy = img.copy()


def calculate_angle(a, b, c):
    # Convert points a and b to vectors and create vector BA
    # BA points from point b to point a
    ba = np.array(a) - np.array(b)

    # Convert points c and b to vectors and create vector BC
    # BC points from point b to point c
    bc = np.array(c) - np.array(b)

    # Compute cosine of the angle between vectors BA and BCQ
    # Dot product gives similarity between directions
    # Norm gives the length (magnitude) of each vector
    cosine_angle = np.dot(ba, bc) / (
        np.linalg.norm(ba) * np.linalg.norm(bc)
    )

    # Apply inverse cosine (arccos) to get angle in radians
    # Convert radians to degrees for easier understanding
    angle = np.degrees(np.arccos(cosine_angle))

    return angle



def mouse_click(event, x, y, flags, param):
    global points, img

    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 3:
        points.append((x, y))

        # 🔵 Bright Blue points
        cv2.circle(img, (x, y), 7, (255, 0, 0), -1)

        # ⚫ Black coordinate text
        # cv2.putText(img, f"{x},{y}", (x + 6, y - 6),
                    # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        print(f"Point {len(points)} selected: ({x}, {y})")

        if len(points) == 3:
            A, B, C = points

            # 🟢 Neon Green lines
            cv2.line(img, B, A, (255, 0, 255), 10)
            cv2.line(img, B, C, (255, 0, 255), 10)

            angle = calculate_angle(A, B, C)

            # 🟣 Purple angle text
            cv2.putText(img, f"Angle: {angle:.2f} deg",
                        (B[0] + 12, B[1] - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 3)

            print(f"✅ Angle at point B: {angle:.2f} degrees")
            points = []

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_click)

while True:
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        img = img_copy.copy()
        points = []
        print("🔄 Reset all points")

    if key == ord('q'):
        cv2.imwrite('output.png',img)
        break

cv2.destroyAllWindows()
