from pupil_labs.real_time_screen_gaze import marker_generator
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from threading import Thread
from pupil_labs.real_time_screen_gaze.gaze_mapper import GazeMapper
import time
from pupil_labs.realtime_api.simple import Device


def create_marker_array():
    array_markers = []
    for markerID in range(4):
        marker_pixels = marker_generator.generate_marker(marker_id=markerID)
        enlarged_april_tag = np.repeat(np.repeat(marker_pixels, 15, axis=0), 15, axis=1)
        array_markers.append(enlarged_april_tag)
        image = Image.fromarray(enlarged_april_tag)
        image.save(f"marker_{markerID}.png")
    return array_markers


def creat_canvas(array_markers):
    print("creating canvas...")
    root = tk.Tk()


    img0 = ImageTk.PhotoImage(image=Image.fromarray(array_markers[0]))
    img1 = ImageTk.PhotoImage(image=Image.fromarray(array_markers[1]))
    img2 = ImageTk.PhotoImage(image=Image.fromarray(array_markers[2]))
    img3 = ImageTk.PhotoImage(image=Image.fromarray(array_markers[3]))

    canvas = tk.Canvas(root, width=1024, height=768)
    canvas.pack()
    canvas.create_image(20, 20, anchor="nw", image=img0)
    canvas.create_image(864, 20, anchor="nw", image=img1)
    canvas.create_image(864, 608, anchor="nw", image=img2)
    canvas.create_image(20, 608, anchor="nw", image=img3)
    root.mainloop()


def begin():
        # device = discover_one_device(max_search_duration_seconds=0.25)
        ip = "172.20.10.3"
        device = Device(address=ip, port=8080)
        if device is None:
            time.sleep(1)
            begin()

        print(f'Connected to {device}. One moment...')
        calibration = device.get_calibration()
        print(calibration)
        gazeMapper = GazeMapper(calibration)
        print(gazeMapper)
        surface = updateSurface(gazeMapper)
        map_gaze_data(device, gazeMapper, surface)



def updateSurface(gazeMapper):
        if gazeMapper is None:
            return
        gazeMapper.clear_surfaces()
        surface = gazeMapper.add_surface(marker_verts(), screen_size())
        return surface


def marker_verts():
    return { 0: [ (20, 20),  # Top left marker corner
                  (140, 20),  # Top right
                  (140, 140),  # Bottom right
                  (20, 140),  # Bottom left
                ],
             1: [ (864, 20),  # Top left marker corner
                  (984, 20),  # Top right
                  (984, 140),  # Bottom right
                  (20, 140),  # Bottom left
                ],
             2: [ (864, 608),  # Top left marker corner
                  (984, 608),  # Top right
                  (984, 728),  # Bottom right
                  (864, 728),  # Bottom left
                ],
             3: [ (20, 608),  # Top left marker corner
                  (140, 608),  # Top right
                  (140, 728),  # Bottom right
                  (20, 728),  # Bottom left
                ], }


def screen_size():
    return (1024, 768)


def get_surface_gaze(device, gaze_mapper, surface):
    while True:
        frame, gaze = device.receive_matched_scene_video_frame_and_gaze()
        result = gaze_mapper.process_frame(frame, gaze)

        for surface_gaze in result.mapped_gaze[surface.uid]:
            print(f"Gaze at {surface_gaze.x}, {surface_gaze.y}")


def map_gaze_data(device, gazeMapper, surface):
    frameAndGaze = device.receive_matched_scene_video_frame_and_gaze(timeout_seconds=1 / 15)
    if frameAndGaze is None:
        return
    else:
        frame, gaze = frameAndGaze
        result = gazeMapper.process_frame(frame, gaze)
        for surface_gaze in result.mapped_gaze[surface.uid]:
            print(f"Gaze at {surface_gaze.x}, {surface_gaze.y}")


def run():
    time.sleep(1)
    array_markers = create_marker_array()

    side_thread = Thread(target=creat_canvas, args=(array_markers,))
    side_thread.start()

    side_thread.join()
    begin()
