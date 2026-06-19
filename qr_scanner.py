import cv2
from pyzbar.pyzbar import decode

def check_url(url):
    if not url.startswith("https"):
        return "Dangerous ❌"

    if len(url) > 50:
        return "Suspicious ⚠️"

    suspicious_words = ["login", "verify", "bank", "free"]
    for word in suspicious_words:
        if word in url.lower():
            return "Suspicious ⚠️"

    return "Safe ✅"

cap = cv2.VideoCapture(0)

print("Press 'q' to exit...")

while True:
    success, frame = cap.read()

    for barcode in decode(frame):
        data = barcode.data.decode("utf-8")
        result = check_url(data)

        cv2.putText(frame, data, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, "Status: " + result, (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        print("Scanned:", data)
        print("Result:", result)

    cv2.imshow("QR Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
