import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def generate_qr(link, file_name):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(link)

    img_1 = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    img_1.save(file_name)

