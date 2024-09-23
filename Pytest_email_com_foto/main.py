#Importar biblioteca para tirar a foto
import cv2
#Importar biblioteca para enviar o e-mail com anexo
import smtplib
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass

# Criar autenticação do usuário
try:
    login = input('Crie seu login: ')
    email_usuario = input('Coloque aqui o seu email: ')
    senha = getpass.getpass('Crie sua senha: ')  # Esconde a senha durante a entrada

    # Comando para tirar foto usando a webcam
    webcam = cv2.VideoCapture(0)
    resultado, imagem = webcam.read()

    if resultado:
        cv2.imshow('Foto', imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Salva a imagem em arquivo para enviar como anexo
        caminho_foto = 'foto_usuario.png'
        cv2.imwrite(caminho_foto, imagem)
    else:
        print('Erro ao capturar a imagem.')

    # Libera a webcam
    webcam.release()

    # Criar função que vai enviar a conta registrada do usuário para e-mail
    def enviar_email():
        # Configuração da mensagem
        msg = MIMEMultipart()
        msg['Subject'] = 'Você acaba de se registrar no PyTest!'
        msg['From'] = 'PyTest@gmail.com' #Substitua pelo seu e-mail
        msg['To'] = email_usuario
        password = 'senha do aplicativo'  # Substitua pela sua senha do app

        # Corpo do e-mail em HTML
        corpo_email = f'''
        <p>Parabéns {login}, você acaba de criar sua nova conta no PyTest.</p>
        <p>A sua senha tem: {len(senha)} caracteres. Obrigado por utilizar nosso sistema e seja bem-vindo!</p>
        '''
        msg.attach(MIMEText(corpo_email, 'html'))

        # Anexar a imagem
        with open(caminho_foto, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{caminho_foto}"')
            msg.attach(part)

        # Conectar ao servidor SMTP e enviar o e-mail
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
        print('Email enviado com sucesso!')

    # Enviar o email
    enviar_email()

except cv2.error as e:
    print(f'Erro com a câmera: {e}')
except smtplib.SMTPException as e:
    print(f'Erro no envio de e-mail: {e}')
except Exception as e:
    print(f'Ocorreu um erro: {e}')
