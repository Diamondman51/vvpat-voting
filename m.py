# def main(cls):
#     o = cls.__new__(cls)
#     def __new__(cls, *args, **kwargs):
#         instance = super(cls.__class__, cls).__new__(cls)
#         instance.__init__(*args, **kwargs)
#         for i in args:
#             if not hasattr(instance, str(i)):
#                 setattr(instance, str(i), i)
#         return instance

#     cls.__new__ = __new__
#     return cls

# @main
# class A:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b

# # @main
# class B(A):
#     l: str
#     m: int
#     def __init__(self, a, b, l, m):
#         super().__init__(a, b)
#         self.l = l
#         self.m = m

# b = B(1, 2, "hello", 3)

# print(b.l)



# import base64
# from PIL import Image
# from io import BytesIO

# # Base64 encoded image data
# base64_image_data = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAK/SURBVDjLbZNNaFRXFMd/72U+dDLNRItGUSeJiagTJ6IQhdhaWoopFCJiF10UBAXpSlHcddHi0oUbkXYRFURE/NiIIjSkpCpdtGoTJG20iUMsMZJokhmqee/de8/p4jmDggcuFw73/s7/nPu/nqrSe/hch6peUZhD6VYUVUCVeNPaEmcwYbn06/nv1gIkiA8cVNhQLOS96ZkyqtVLEMMEFZgvv2IhVEQTrbyJGAA7i4U13qeda8ivLKIxAVGJq0pcfVljhsyiBDt2f8s7AFSXFDuauXVvjLm516gIAFJVoYqKMl95TRBGvB1vWsBLpBKs29RMe9NSnANVQURxTnEiWFEWAsPlq4PvAyjOCRPTFVJ+kiAIMGGElThvqSORTFFID3Oy+xfqdnUyfLZHvWByX3UGiBOsM4RhyJ5t7bH8WB2qyp27fWxLP2dx8RtyrVuYL61n9Oe+EzUFxgnOWKzzuTD4F6GxWKc4K7Sk/2DPpjINuR3Mjv9Nyov4oGEF2Q/zuRrAWiEyhkhA/TReMgm+sjr1gL0bZ2lc20M4dYlUxmNiaBQTRC+Dhf+6q0PEWIcNLKFxWCcYJ6zkPl93lMi19RJM/oSfsiSzzQSzI4j1P+862v/YrylwggkNoXEExrGkfJuv2sbJtfcSTP6InzRElRaeDtzj+4EGth7tHwLw327BRDGgsXKXL/LPWN7xJdHzPupSSlhpZur2fX4Y+Yyx+XTtGf2qYSLrsKGl/lk/vflphFVMPTyFEPBqdhWlwYdcW3SYF1H2vUaKDRM5CjpA4aMzPLp0jMd3fiOd30x5ZoqbyYNkMktRxhCRp+8oUFXwfbq2d/JofIZo5Aatmz+mvn49//75D0NNh8g2tWGtoAphENbs6Kkqn+w/3afKAUVZ8eQ4W1uX0bWhhYmonqulTuZMtvYzUa7/fvHI7irgf/y+taODWkwAAAAAAElFTkSuQmCC"

# # Decode the base64 string
# image_data = base64.b64decode(base64_image_data)

# # Create an image from the decoded bytes
# image = Image.open(BytesIO(image_data))

# # Display the image
# image.show()


class P:
    pass


p = P()
p.a = 1

print(p.a)


import asyncio
import time

async def delayed_function():
    await asyncio.sleep(5)  # Wait for 2 seconds
    print("Executed after 5 seconds")


async def t2():
    print("Executed after 0 seconds")


async def test():
    await asyncio.sleep(3)   


async def main2():
    await asyncio.sleep(4)
    print('Executed after 4 seconds')


async def main():
    await asyncio.gather(delayed_function(), test(), t2(), main2())

asyncio.run(main())  # Runs the async function
