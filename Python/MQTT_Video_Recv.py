# coding: UTF-8
import time
import cv2
import numpy as np
import paho.mqtt.client as paho
import Queue

is_cv3 = ( cv2.__version__[0] == '3' )

MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "/rcr/video"
messages = Queue.Queue()

def mqtt_on_message( client, userdata, message ):
    global MQTT_SERVER, MQTT_TOPIC

    # ponemos el mensaje en la cola para procesamiento posterior
    messages.put_nowait( message )

def mqtt_on_connect( client, arg1, arg2, arg3 ):
    global MQTT_SERVER, MQTT_TOPIC

    # nos suscribimos al topico que nos interesa
    client.subscribe( MQTT_TOPIC )

def main():
    global is_cv3, MQTT_SERVER, MQTT_TOPIC, messages

    # establecemos ventana y dimensiones
    winName = 'Video In'
    imgH,imgW = 240, 320
    if( is_cv3 ):
        cv2.namedWindow( winName, cv2.WINDOW_AUTOSIZE )
    else:
        cv2.namedWindow( winName, cv2.CV_WINDOW_AUTOSIZE )
    cv2.resizeWindow( winName, imgW, imgH )

    # nos conectamos al servidor MQTT
    mqtt_client = paho.Client()
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    # cv2 y cv3 tienen incompatibilidades
    if( is_cv3 ):
        LOAD_IMAGE_COLOR = cv2.IMREAD_COLOR
    else:
        LOAD_IMAGE_COLOR = cv2.CV_LOAD_IMAGE_COLOR

    # procesamos hasta que recibamos ESC
    while True:
        # recibimos un frame
        try:
            message = messages.get_nowait()
            data = np.fromstring( message.payload, np.uint8 )
            frame = cv2.imdecode( data, LOAD_IMAGE_COLOR )

            # mostramos el frame
            cv2.imshow( winName, frame )
        except Queue.Empty:
            pass
        except Exception as e:
            print e

        # verificamos si se presiona ESC
        if( cv2.waitKey( 5 ) == 27 ):
            break

    # eso es todo
    mqtt_client.loop_stop()
    cv2.destroyAllWindows()


# Show time
main()
