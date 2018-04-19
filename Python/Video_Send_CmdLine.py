# coding: UTF-8
from __future__ import print_function
import time
import cv2
import numpy as np
import paho.mqtt.client as paho

G_IS_CV3 = ( cv2.__version__[0] == '3' )

#### Cambiar aqui
G_DEVICE = 0
G_WIDTH = 320
G_HEIGHT = 240
G_FPS = 10
#G_MQTT_SERVER = "iot.eclipse.org"
G_MQTT_SERVER = "test.mosquitto.org"
G_MQTT_PORT = 1883
G_MQTT_TOPIC = "rcr/video"
####

def main():
    # abrimos dispositivo de captura
    cap = cv2.VideoCapture( G_DEVICE )

    # dimensiones de la captura
    if( G_IS_CV3 ):
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, G_HEIGHT )
        cap.set( cv2.CAP_PROP_FRAME_WIDTH, G_WIDTH )
    else:
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, G_HEIGHT )
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, G_WIDTH)

    # el servidor MQTT
    mqtt_client = paho.Client()
    mqtt_client.connect( G_MQTT_SERVER, G_MQTT_PORT )

    # iniciamos la captura
    print( 'Iniciando captura y envio. Presione Ctrl-C para abortar' )
    delay = 1./G_FPS
    t1 = time.time()
    while( True ):
        try:
            # 1. se captura rapido pues internamente hay un buffer que puede producir lags a bajos FPS
            # 2. poca luz genera demoras en la decodificación
            ret, img = cap.read()
            if( ret ):
                t2 = time.time()
                if( ( t2 - t1 ) >= delay ):
                    data = cv2.imencode( '.jpg', img )[1].tostring()
                    mqtt_client.publish( G_MQTT_TOPIC, data )
                    t1 = t2
        except KeyboardInterrupt:
            break
        except Exception as e:
            print( str( e ) )
        time.sleep( 0.010 )

    # liberamos el dispositivo de captura
    mqtt_client.disconnect()
    cap.release()


# Show time
main()

