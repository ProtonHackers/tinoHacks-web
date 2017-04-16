import os
import numpy as np

STREAM_PATH = "stream"
PREVIOUS_ACTION_PATH = "action"

ZERO_ACC = np.array([0, 0, 0])
STOP_ERROR_DISTANCE_CONSTANT = 1

MIN_CHUNK_SIZE = 100
TRIGGER_ACTION = np.array([0, 2])

def save_coordinate_to_npy(x, y, z):
    if os.path.exists(STREAM_PATH):
        stream = np.load(STREAM_PATH)
    else:
        stream = np.array([[x, y, z]])
    np.save(STREAM_PATH, stream)

def magnitude(acc3D):
    return np.linalg.norm(acc3D - ZERO_ACC)

def stopped(acc3D):
    return magnitude(acc3D) <= STOP_ERROR_DISTANCE_CONSTANT

def load_coordinate_stream(x, y, z):
    stream = np.load(STREAM_PATH)

    if os.path.exists(PREVIOUS_ACTION_PATH):
        previous_action = np.load(PREVIOUS_ACTION_PATH)

        if stopped(np.array([x, y, z])) and len(stream) >= MIN_CHUNK_SIZE:
            accel_vector = convert_points_to_vector(stream)
            classification = classify_action(accel_vector)

            if np.array([previous_action[0], classification[0]]) == TRIGGER_ACTION:
                # TODO send post request
                pass
            np.save(PREVIOUS_ACTION_PATH, classification)
            np.save(STREAM_PATH, np.array([]))

def convert_points_to_vector(stream):
    return max(stream, key=lambda x: magnitude(x))

# TODO Vikranth
def classify_action(vector):
    return np.array([0])