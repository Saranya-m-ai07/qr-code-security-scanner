from flask import Flask, render_template, request
import cv2

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        file = request.files["qrfile"]

        file.save("uploaded.png")

        img = cv2.imread("uploaded.png")

        detector = cv2.QRCodeDetector()

        data, bbox, straight_qrcode = detector.detectAndDecode(img)

        if data:

            score = 0

            if not data.startswith("https://"):
                score += 30

            suspicious_words = [
                "login",
                "verify",
                "password",
                "bank",
                "free",
                "winner"
            ]

            for word in suspicious_words:
                if word in data.lower():
                    score += 20

            if score < 30:
                result = f"SAFE ✅ : {data}"

            elif score < 60:
                result = f"SUSPICIOUS ⚠️ : {data}"

            else:
                result = f"DANGEROUS 🚨 : {data}"

        else:
            result = "No QR Code Found"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)
