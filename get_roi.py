import cv2

points = []

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"{x}, {y}")
        points.append((x, y))

        cv2.circle(frame, (x, y), 5, (0,0,255), -1)
        cv2.imshow("Frame", frame)


frame = cv2.imread("D:\\SSDP\\traffic\\traff.png")   # use your screenshot or frame

cv2.imshow("Frame", frame)
cv2.setMouseCallback("Frame", mouse_click)

cv2.waitKey(0)
cv2.destroyAllWindows()

print("\nROI points:")
print(points)