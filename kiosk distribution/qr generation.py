import random
import qrcode
import os

# 6 xonali sonni generatsiya qilish
def generate_six_digit_number():
    return random.randint(100000, 999999)

six_digit_number = generate_six_digit_number()

# QR kodni yaratish
def create_qr_code(data, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)  # Katalog mavjud bo'lmasa, yaratadi

    file_path = os.path.join(directory, filename)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # QR kodni PNG fayliga saqlash
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    return file_path

# QR kod yaratish
output_directory = "kiosk distribution/image qrcode"  # Fayl saqlanadigan katalog
qr_filename = f"qr{six_digit_number}.png"

file_path = create_qr_code(str(six_digit_number), output_directory, qr_filename)

print(f"6 xonali son: {six_digit_number}")
print(f"QR kod fayli saqlandi: {file_path}")
