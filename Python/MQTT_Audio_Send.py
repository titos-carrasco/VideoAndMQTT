# coding: UTF-8
import time
import pysoundcard
import numpy as np
import paho.mqtt.client as paho
import threading
import Queue

g_running = False
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

def _TSendAudioChunk():
    global MQTT_SERVER, MQTT_PORT, MQTT_TOPIC, g_running, g_messages

    mqtt_client = paho.Client()
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    while( g_running ):
        try:
            data = g_messages.get_nowait()
            mqtt_client.publish( MQTT_TOPIC, data )
        except Queue.Empty:
            pass
        except Exception as e:
            print e
        time.sleep( 0.001 )
    mqtt_client.loop_stop()


def main():
    global AUDIO_FS, AUDIO_FRAMES, AUDIO_CHANNELS, AUDIO_DTYPE, g_running, g_messages

    g_running = True
    tSendAudioChunk = threading.Thread( target=_TSendAudioChunk, args=(), name="_TSendAudioChunk" )
    tSendAudioChunk.start()

    istream = pysoundcard.InputStream( samplerate=AUDIO_FS,
                                       blocksize=AUDIO_FRAMES,
                                       channels=AUDIO_CHANNELS,
                                       dtype=AUDIO_DTYPE )
    istream.start()

    print
    print "Presione CTRL-C para finalizar"
    while( True ):
        try:
            data = istream.read( AUDIO_FRAMES ).tostring()
            g_messages.put_nowait( data )
        except KeyboardInterrupt:
            break
        except Exception as e:
            print e
        time.sleep( 0.001 )

    # finalizamos las tareas
    g_running = False
    tSendAudioChunk.join()

    # liberamos el dispositivo
    istream.stop()


# show time
main()
