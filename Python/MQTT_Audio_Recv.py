# coding: UTF-8
import time
import cv2
import pysoundcard
import numpy as np
import paho.mqtt.client as paho
import Queue

g_messages = Queue.Queue()

# Configure here your connection parameters
#
MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/audio"

AUDIO_FS = 11025
AUDIO_FRAMES = 256
AUDIO_CHANNELS = 1
AUDIO_DTYPE = 'int16'
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
    global MQTT_SERVER, MQTT_PORT, AUDIO_FS, AUDIO_FRAMES, AUDIO_CHANNELS, AUDIO_DTYPE, g_messages

    # nos conectamos al servidor MQTT
    mqtt_client = paho.Client()
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    # el stream de audio
    ostream = pysoundcard.OutputStream( samplerate=AUDIO_FS,
                                        #blocksize=AUDIO_FRAMES,
                                        channels=AUDIO_CHANNELS,
                                        dtype=AUDIO_DTYPE )
    ostream.start()

    print
    print "Presione CTRL-C para finalizar"
    while True:
        try:
            # recibimos un chunk
            message = g_messages.get_nowait()
            data = np.fromstring( message.payload, np.int16 )

            # lo reproducimos
            ostream.write( data )
        except Queue.Empty:
            pass
        except KeyboardInterrupt:
            break
        except Exception as e:
            print e
        time.sleep( 0.001 )

    # eso es todo
    mqtt_client.loop_stop()
    ostream.stop()

# Show time
main()
