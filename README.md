# VideoAndMQTT
Use MQTT to send and receive audio/video

* Html/:
    * MQTT_Video_Recv.html; html/javascript to show video frames received via websockets
* NodeRed/:
  * MQTT_WSocket_NodeRed.flow; flow to get video frames from an MQTT broker and send it using websockets
* Python/: 
  * MQTT_Video_Send.py; capture, display and send video frames
  * MQTT_Video_Recv.py; receive and display video frames
  * MQTT_Audio_Send.py; capture and send audio chunks
  * MQTT_Audio_Recv.py; receive and play audio chunks

To DO
* Needs documentation
* GUI 
* Android APP
* 