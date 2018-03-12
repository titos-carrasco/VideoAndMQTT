# coding: UTF-8
import time
import cv2
import numpy as np
import paho.mqtt.client as paho

is_cv3 = ( cv2.__version__[0] == '3' )

MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "/rcr/video"

def main():
    global is_cv3, MQTT_SERVER, MQTT_TOPIC

    # abrimos dispositivo de captura
    device = 0
    cap = cv2.VideoCapture( device )

    # establecemos ventana y dimensiones de la captura
    winName = 'Video Out'
    imgH,imgW = 240, 320
    if( is_cv3 ):
        cv2.namedWindow( winName, cv2.WINDOW_AUTOSIZE )
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, imgH )
        cap.set( cv2.CAP_PROP_FRAME_WIDTH, imgW )
    else:
        cv2.namedWindow( winName, cv2.CV_WINDOW_AUTOSIZE )
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, imgH )
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, imgW )
    cv2.resizeWindow( winName, imgW, imgH )

    # ticks por segundos (para desplefar fps)
    tps = cv2.getTickFrequency()

    # nos conectamos al servidor MQTT
    mqtt_client = paho.Client()
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    # procesamos hasta que recibamos ESC
    t1=cv2.getTickCount()
    while True:
        # capturamos un cuadro
        ret, frame = cap.read()
        if( not ret ):
            break

        # lo enviamos al servidor MQTT como JPG
        data = cv2.imencode('.jpg', frame)[1].tostring()
        mqtt_client.publish( MQTT_TOPIC, data )

        # lo mostramos
        t2=cv2.getTickCount()
        cv2.putText(frame, "%04.2f FPS" % (1/((t2-t1)/tps)), (10, imgH-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.imshow( winName, frame )
        t1=t2

        # verificamos si se presiona ESC
        if( cv2.waitKey( 5 ) == 27 ):
            break

        # controlamos la velocidad de captura
        time.sleep( 0.250 )

    # eso es todo
    mqtt_client.loop_stop()
    cap.release()
    cv2.destroyAllWindows()


# Show time
main()
