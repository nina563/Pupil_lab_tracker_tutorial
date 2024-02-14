# Pupil_lab_tracker_tutorial
This tutorial shows how to create an experiment in Openseame with an integrated Pupil Lab eye-tracking device. We use Python inline coding. The example of the Opensesame experiment with integrated tracker is provided.

## Table of Contents
1. [Resources](#heading--1)
2. [Connecting to the eye-tracking device](#heading--2)
3. [Starting the recording](#heading--3)
4. [Saving events](#heading--4)
5. [Stop the recording](#heading--5)
6. [Processing the recordings](#heading--6)
7. [Opensesame template](#heading--7)

## Resources <div id="heading--1"/>
- ADD

## Connecting to the eye-tracking device <div id="heading--2"/>

To connect the laptop/PC to the tracker you will need to connect both devices to the same [local network](https://docs.pupil-labs.com/invisible/real-time-api/tutorials/). For discovery, the local network must allow MDNS and UDP traffic. In large public networks, this may be prohibited for security reasons. Alternatively, the hotspot can be created using a third device - neither the Companion phone nor the laptop you are using to run Opensesame.

Pupil Lab provides a [real-time API](https://github.com/pupil-labs/realtime-network-api), that allows you to control the tracking device. 

You can use pip to install the library through the Opensesame console:
```
pip install pupil-labs-realtime-api
```

Opensesame provides `inline_script` item. We will use them to add Python code to the experiment body. Use further code snippet in the **Prepare** phase of the `inline_script` to initialize the tracking device. 
> To check the IP of the Neon device, go to the settings of the phone, navigate to **About device** -> **Status**, and you will find the IP address.

```
from pupil_labs.realtime_api.simple import Device
ip = “ip of the Neon device "
device = Device(address=ip, port=8080)
```
You can check if the connection was set by printing out a status update from the device:
```
print(f"Phone IP address: {device.phone_ip}")
print(f"Phone name: {device.phone_name}")
print(f"Phone unique ID: {device.phone_id}")
```
## Starting the recording <div id="heading--3"/>
To start the recording you need to have this code in the **Run** phase of the  `inline_script` item:
```
recording_id = device.recording_start()
print(f"Started recording with id {recording_id}”)
```
## Saving events <div id="heading--4"/>
While recording is running, you can create events using the save_event() method. 
```
device.send_event("test event 2", event_timestamp_unix_ns=time.time_ns())
```
> Optionally, you can set a custom timestamp for your event, instead of using the time of the arrival, as in the example. 

## Stop the recording <div id="heading--5"/>
Use the recording_stop_and_save() method to stop the recording:
```
device.recording_stop_and_save()
device.close()
```

## Processing the recordings <div id="heading--6"/>
After stopping and saving, the recording will automatically uploaded to the Pupil Cloud. For analysing the gaze data of the experiment participants, the data need to be mapped to the defined surface. Pupil Cloud enrichment [Marker Mapper](https://docs.pupil-labs.com/neon/pupil-cloud/enrichments/marker-mapper/#surface-positions-csv) enables that. Further, the remapped gaze data can be downloaded in [CVS](https://docs.pupil-labs.com/neon/data-collection/data-format/) format. 

For defining the surface of the PC screen we use the April Tags 36H11 family. We have 4 tags on the corners of the Opensesame canvas throughout the experiment.



<p align="center">
  <img width="439" alt="Screenshot 2024-02-14 at 13 48 08" src="https://github.com/nina563/Pupil_lab_tracker_tutorial/assets/83282861/8755f306-0e6e-448c-bcf2-e48a13d75998">
</p>

#### Steps to process the video in the Pupil Cloud :
1. Create a project in your workspace 
2. Add recording to the project 
3. On the project page, navigate to Enrichments, press `Create enrichment`, choose `Marker Mapper` and press **create**.
   
>You might need to move a few frames forward or backward to get the April tags detected.
>


<p align="center">
<img width="1440" alt="Screenshot 2024-02-14 at 13 54 09" src="https://github.com/nina563/Pupil_lab_tracker_tutorial/assets/83282861/ca8de90f-7db7-466e-848f-712c03563cc3">
</p>

4. After giving a name to the surface and defining it, press `Run` button on the top left corner to start the video processing. 
5. At the end the mapped gaze data can be found for download at the `Downloads` tab under **Enrichment data**.

<p align="center">
  <img width="1439" alt="Screenshot 2024-02-14 at 15 03 07" src="https://github.com/nina563/Pupil_lab_tracker_tutorial/assets/83282861/eead8f52-560e-44ea-b47d-04578d417474">
</p>

## Opensesame template <div id="heading--7"/>
The provided Opensesame example experiment shows a viewer an image and the correspondent should choose if the image is AI-generated or real. The recording starts right before the instruction sketchpad is shown and ends after the last image. When the new image is shown, we save the timestamp of the event.


#### Run the example file
To run the example file: 
- You need to download the image folders (**fake**, **real**, **april_tag**) and save them to the same folder as the .osexp experiment file. 
- Pip install the real-time API in the Opensesame console.
- Connect laptop/PC to the same local network as Neon companion device

After that, you are ready to run the example experiment!
