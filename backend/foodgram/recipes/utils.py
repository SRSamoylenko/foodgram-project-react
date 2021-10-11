import codecs


def get_decoded_image(data: str) -> bytes:
    image_str = data.split(',')[-1]
    image_binary = image_str.encode('utf-8')
    return codecs.decode(image_binary, 'base64')
