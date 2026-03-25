import pyttsx3                              # Esta biblioteca hace que el sistema se comunique con nosotros
import speech_recognition as sr             # Esta biblioteca permite que el sistema reconozca el sonido de nuestra voz y lo pase a texto
import pywhatkit                            # Esta biblioteca permite que el sistema abra sitios como youtube, wikipedia, etc
import yfinance as yf                       # Esta biblioteca permite conectarse las bolsas de valores
import pyjokes                              # Esta biblioteca permite hacer bromas
import webbrowser                           # Esta biblioteca permite usar el navegador de internat
import datetime                             # Esta biblioteca da fecha y hora
import wikipedia                            # Esta biblioteca permite acceder a wikipedia

# Opciones de voz e idioma
id1= 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2= 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0 '
id3= 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'



#Escuchar el microfono y devolver el audio como texto
def transformar_audio_en_texto():

    # Almacenar recognizer envariable
    reconocer = sr.Recognizer()

    # Configurara el microfono
    with sr.Microphone() as origen:

        # Tiempo de espera para que arranque, esto se usa para que no haya errores con el audio
        reconocer.pause_threshold = 0.8                 #Es la pausa al arrancar el programa

        # Informar que ya comenzo la grabación
        print('Ya puedes hablar')

        # Guardar lo que se escuche como audio
        audio = reconocer.listen(origen)

        try:
            # Buscar en google (Lo que se hace es pasar a texto lo que se haya encontrado)
            pedido = reconocer.recognize_google(audio, language='es-VE')        #No te pone el google pero si lo reconoce

            # Prueba de que aceptó nuestro audio y lo paso a texto
            print('Dijiste: ' + pedido)

            # Devolver pedido
            return pedido
        
        # En caso de que no se comprenda el audio
        except sr.UnknownValueError:

            # Prueba de que no comprendio el audio
            print('Ups, no entendi')

            # Devolver error
            return 'Sigo esperando...'
        
        # En caso de no resolver el pedido
        except sr.RequestError:

            # Prueba de que no comprendio el audio
            print('Ups, no hay servicio')

            # Devolver error
            return 'Sigo esperando...'
        
        # En caso de error inesperado
        except:

            # Prueba de que no comprendio el audio
            print('Ups, algo ha salido mal')

            # Devolver error
            return 'Sigo esperando...'
        

#Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # Encender el motor de pyttsx3
    engine = pyttsx3.init()         # Esto es para inicializar la libreria
    engine.setProperty('voice', id2)

    #Pronunciar mensaje
    engine.say(mensaje)             # Esto es para que pronuncie el mensaje
    engine.runAndWait()             # Esto es para que ejecute el comando y espere


# Informar día de semana
def pedir_dia():

    # Crear variable con datos de hoy
    dia = datetime.date.today()            # Cuando se quiere trabajr con el día actual se usa datetime.date.today()
    print(dia)

    # Crear variable para el día de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario con los nombres de los días
    calendario = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles',
                  3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    
    # Decir el día de la semana
    hablar(f'Hoy es: {calendario[dia_semana]}')


# Pedir que hora es
def pedir_hora():

    # Creamos la varaible de la hora
    hora = datetime.datetime.now()          #Cuando se quiere trabajar con la hora se debe usar datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # Decir la hora del día
    hablar(hora)


# Hacer el saludo inicial
def saludo_inicial():

    # Crera variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else: 
        momento = 'Buenas tardes'

    # Decir el saludo
    hablar(f'{momento}, soy Helena, tu asistente virtual. En que puedo ayudarte?')


# Funcion para oedir cosas
def pedir_cosas():

    # Activamos el saludo inicial
    saludo_inicial()

    # Variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # Activamos el micro y se guarda el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir google' in pedido:
            hablar('Con gusto, estoy abriendo google')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('wikipedia dice lo siguiente')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('ya estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo quehe encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL', 'amazon':'AMZN', 'google':'GOOGL'}

            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'la encontre, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdon pero no la he encontrado')
        elif 'adiós' in pedido:
            hablar('Ok, voy a descansar')
            break




pedir_cosas()




    






