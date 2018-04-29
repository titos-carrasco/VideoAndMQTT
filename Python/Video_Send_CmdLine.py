# coding: UTF-8
from __future__ import print_function
import time
import cv2
import numpy as np
import paho.mqtt.client as paho
import argparse

G_IS_CV3 = ( cv2.__version__[0] == '3' )
if( G_IS_CV3 ):
    G_IMWRITE_JPEG_QUALITY = cv2.IMWRITE_JPEG_QUALITY
else:
    G_IMWRITE_JPEG_QUALITY = cv2.cv.CV_IMWRITE_JPEG_QUALITY

#### Capture Video Frame Dimension
G_WIDTH = 320
G_HEIGHT = 240
####

def main():
    parser = argparse.ArgumentParser( description="Capture video and send it to an MQTT server" )
    parser.add_argument( "video_device", help="video device index ( 0, 1, ... )", type=int )
    parser.add_argument( "mqtt_server", help="MQTT Server" )
    parser.add_argument( "--mqtt_port", help="MQTT Port (default: 1883)", type=int )
    parser.add_argument( "mqtt_topic", help="MQTT topic" )
    parser.add_argument( "--fps", help="video frames per second ( 1<=>30, default: 10)", type=int )
    parser.add_argument( "--jpeg_quality", help="video jpeg quality ( 0<=100, default: 30)", type=int )
    args = parser.parse_args()

    if( args.video_device < 0 ):
        print( "Error: invalid video device index: {}".format( args.video_device ) )
        return

    if( args.mqtt_port is None ):
        args.mqtt_port = 1883
    elif( args.mqtt_port < 0 or args.mqtt_port > 65535 ):
        print( "Error: invalid MQTT Port: {}".format( args.mqtt_port ) )
        return

    if( args.fps is None ):
        args.fps = 10
    elif( args.fps <= 0 or args.fps > 30 ):
        print( "Error: invalid frames per second: {}".format( args.fps ) )
        return

    if( args.jpeg_quality is None ):
        args.jpeg_quality = 30
    elif( args.jpeg_quality < 0 or args.jpeg_quality > 100 ):
        print( "Error: invalid jpeg quality: {}".format( args.jpeg_quality ) )
        return

    doTransmit( args.video_device, args.mqtt_server, args.mqtt_port, args.mqtt_topic, args.fps, args.jpeg_quality )


def doTransmit( p_video_device, p_mqtt_server, p_mqtt_port, p_mqtt_topic, p_fps, p_jpeg_quality ):
    # abrimos dispositivo de captura
    try:
        cap = cv2.VideoCapture( p_video_device )
    except Exception as e:
        print( e )
        return
    if( p_video_device<0 or not cap.isOpened() ):
        print( 'Error: invalid device index => {}'.format( p_video_device ) )
        return

    # dimensiones de la captura
    if( G_IS_CV3 ):
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, G_HEIGHT )
        cap.set( cv2.CAP_PROP_FRAME_WIDTH, G_WIDTH )
    else:
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, G_HEIGHT )
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, G_WIDTH)

    # el servidor MQTT
    mqtt_client = paho.Client()
    try:
        mqtt_client.connect( p_mqtt_server, p_mqtt_port )
    except Exception as e:
        print( "Error: can't connect to MQTT Server => {}:{}".format( p_mqtt_server, p_mqtt_port ) )
        print( e )
        return

    # iniciamos la captura
    print( 'Iniciando captura y envio a mqtt://{}:{}/{}'.format( p_mqtt_server, p_mqtt_port, p_mqtt_topic ) )
    print( 'FPS={}, JPEG_QUALITY={}'.format( p_fps, p_jpeg_quality ) )
    print( '=== Presione Ctrl-C para abortar ===' )
    delay = 1./p_fps
    t1 = 0.
    while( True ):
        try:
            # 1. se captura rapido pues internamente hay un buffer que puede producir lags a bajos FPS
            # 2. poca luz genera demoras en la decodificación
            ret, img = cap.read()
            if( ret ):
                t2 = time.time()
                if( ( t2 - t1 ) >= delay ):
                    data = cv2.imencode( '.jpg', img, ( G_IMWRITE_JPEG_QUALITY, p_jpeg_quality ) )[1].tostring()
                    mqtt_client.publish( p_mqtt_topic, data )
                    t1 = t2
        except KeyboardInterrupt:
            break
        except Exception as e:
            e = str( e )
            print( "Error: {}".format( e ) )
            if( e == "Invalid topic." ):
                break
        time.sleep( 0.010 )

    # liberamos el dispositivo de captura
    mqtt_client.disconnect()
    cap.release()


# Show time
if __name__ == '__main__':
    main()

