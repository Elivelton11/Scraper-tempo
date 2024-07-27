from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurar opções do Chrome para ignorar erros de certificado
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Abrir um navegador e acessar o site de previsão do tempo
driver = webdriver.Chrome(options=options)
driver.get('https://www.tempo.com/criciuma.htm')
sleep(10)

# Extrair a temperatura atual
try:
    temperatura_element = driver.find_element(By.XPATH, "//span[@class='dato-temperatura changeUnitT']")
    temperatura = temperatura_element.text
    print(f"Temperatura atual: {temperatura}")
except Exception as e:
    print(f"Erro ao extrair a temperatura: {e}")

# Extrair a condição atual do tempo
try:
    tempo_element = driver.find_element(By.XPATH, "//span[@class='descripcion']")
    tempo = tempo_element.text
    print(f"Condição atual: {tempo}")
except Exception as e:
    print(f"Erro ao extrair a condição do tempo: {e}")

# Extrair a previsão para os próximos 3 dias (temperatura e condição)
try:
    previsao1_temp = driver.find_element(By.XPATH, "//li[@class='grid-item dia d2']//span[@class='max changeUnitT']").text
    previsao1_cond = driver.find_element(By.XPATH, "//li[@class='grid-item dia d2']//span[@class='min changeUnitT']").text
    print(f"Previsão dia 1 - Máx: {previsao1_temp}, Mín: {previsao1_cond}")
except Exception as e:
    print(f"Erro ao extrair a previsão do dia 1: {e}")

try:
    previsao2_temp = driver.find_element(By.XPATH, "//li[@class='grid-item dia d3']//span[@class='max changeUnitT']").text
    previsao2_cond = driver.find_element(By.XPATH, "//li[@class='grid-item dia d3']//span[@class='min changeUnitT']").text
    print(f"Previsão dia 2 - Máx: {previsao2_temp}, Mín: {previsao2_cond}")
except Exception as e:
    print(f"Erro ao extrair a previsão do dia 2 : {e}")

try:
    previsao3_temp = driver.find_element(By.XPATH, "//li[@class='grid-item dia d4']//span[@class='max changeUnitT']").text
    previsao3_cond = driver.find_element(By.XPATH, "//li[@class='grid-item dia d4']//span[@class='min changeUnitT']").text
    print(f"Previsão dia 3 - Máx: {previsao3_temp}, Mín: {previsao3_cond}")
except Exception as e:
    print(f"Erro ao extrair a previsão do dia 3 : {e}")

# Fechar o navegador
driver.quit()


# Configuração do servidor SMTP do Gmail

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'eliveltopadilhaa@gmail.com'
smtp_password = 'eiag qpdx iuee brwv'

#Criar a mensagem do email

msg = MIMEMultipart()
msg['From'] = smtp_user
msg['To'] = 'eliveltonpadilhaa@hotmail.com'
msg['Subject'] = 'Dados de previsão do tempo'

#Corpo do email

corpo_html = f"""

<html>
<head></head>
<body>
    <p>Prezado(a), estamos encaminhando para você a previsão do tempo atual e dos próximos 3 dias para fins de conhecimento: </p>
    <p>Nesse exato momento a temperatura é de {temperatura}, condição atual do tempo é {tempo}</p>
    <p>Previsão para o dia 1: {previsao1_temp}</p>
    <p>Previsão para o dia 2: {previsao2_temp}</p>
    <p>Previsão para o dia 3: {previsao3_temp}</p>


</body>
</html>
"""

#Anexar o corpo HTML ao email
msg.attach(MIMEText(corpo_html,'html'))

#Enviar o email

try:
    #Conectar ao servidor SMTP
    server = smtplib.SMTP(smtp_server,smtp_port)
    server.starttls() #Ativar a segurança TLS
    server.login(smtp_user, smtp_password) #login
    texto = msg.as_string() #Converter a mensagem para string
    server.sendmail(msg['From'], msg['To'], texto) #Enviar o email
    print('E-mail enviado com sucesso!')

except Exception as e: 
    print(f'Erro ao enviar o e-mail: {e}')
finally:
    server.quit() #Fechar a conexão com o servidor
