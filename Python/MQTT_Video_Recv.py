# coding: UTF-8
from __future__ import print_function
import time
import cv2
import numpy as np
import paho.mqtt.client as paho
import Queue

IS_CV3 = ( cv2.__version__[0] == '3' )
g_messages = Queue.Queue()

WIN_CAPTURE = "Video In"

# Configure here your connection parameters
#
MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/video"
#
# End configuration

def mqtt_on_message( client, userdata, message ):
    global g_messages

    # ponemos el mensaje en la cola para procesamiento posterior
    g_messages.put_nowait( message )

def mqtt_on_connect( client, arg1, arg2, arg3 ):
    global MQTT_TOPIC

    # nos suscribimos al topico que nos interesa
    client.subscribe( MQTT_TOPIC )

def main():
    global IS_CV3, g_messages, WIN_CAPTURE, MQTT_SERVER, MQTT_PORT

    # establecemos ventana y dimensiones
    imgH,imgW = 240, 320
    if( IS_CV3 ):
        cv2.namedWindow( WIN_CAPTURE, cv2.WINDOW_AUTOSIZE )
        LOAD_IMAGE_COLOR = cv2.IMREAD_COLOR
    else:
        cv2.namedWindow( WIN_CAPTURE, cv2.CV_WINDOW_AUTOSIZE )
        LOAD_IMAGE_COLOR = cv2.CV_LOAD_IMAGE_COLOR
    cv2.resizeWindow( WIN_CAPTURE, imgW, imgH )

    # nos conectamos al servidor MQTT
    mqtt_client = paho.Client()
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    # procesamos hasta que recibamos ESC
    while True:
        try:
            # recibimos un frame
            message = g_messages.get_nowait()
            data = np.fromstring( message.payload, np.uint8 )
            frame = cv2.imdecode( data, LOAD_IMAGE_COLOR )

            # mostramos el frame
            cv2.imshow( WIN_CAPTURE, frame )
        except Queue.Empty:
            pass
        except Exception as e:
            print( e )

        # verificamos si se presiona ESC
        if( cv2.waitKey( 1 ) == 27 ):
            break

    # eso es todo
    mqtt_client.loop_stop()
    cv2.destroyAllWindows()


# Show time
main()
