import qrcode
qrcode_usuario = input('Bem vindo ao gerador de QRcode, qual site você deseja gerar em QR? ')
img = qrcode.make(f'https://{qrcode_usuario}.com')

img.save('qrcode_1.png')




