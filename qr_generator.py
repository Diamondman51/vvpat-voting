import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

# Saylovchi ma'lumotlari
voter_data = """Saylovchi ID: 12345
Ism: John Doe
Nomzod: Prezident
Saylov Joyi: Markaz A
Vaqti: 2024-11-23"""

# QR kod yaratish
qr = qrcode.QRCode(
    version=2,  # Bu yerda versiya oshirilgan, ma'lumotni ko'proq saqlash uchun
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Xato tuzatish darajasini oshirish
    box_size=10,
    border=4,
)

qr.add_data(voter_data)
qr.make(fit=True)

# QR kodni tasvirga aylantirish
img = qr.make_image(fill='green', back_color='white')

# QR kodni saqlash
img.save("voter_qr_with_logo.png")

# QR kodni tasvirdan o'qish
img = Image.open("voter_qr_with_logo.png")

# QR kodni dekodlash
decoded_objects = decode(img)

# QR koddan o'qilgan ma'lumotni chiqarish
for obj in decoded_objects:
    decoded_data = obj.data.decode('utf-8')
    print(f"O'qilgan ma'lumot: {decoded_data}")

    # Saylovchi ID va saylov joyini tahlil qilish
    if "Saylov Joyi" in decoded_data:
        print("Saylov joyi: Markaz A")
    else:
        print("Ma'lumotni tahlil qilishda xato yuz berdi.")