import os
import numpy as np
import math

STREAM_PATH = "stream"
PREVIOUS_ACTION_PATH = "action"

ZERO_ACC = np.array([0, 0, 0])
STOP_ERROR_DISTANCE_CONSTANT = 1

MIN_CHUNK_SIZE = 100
TRIGGER_ACTION = np.array([0, 2])

UP_ACTION = 0
DOWN_ACTION = 1
RIGHT_ACTION = 2
LEFT_ACTION = 3
FORWARD_ACTION = 4
BACK_ACTION = 5

# Watch face up and hand extended forward
# Values from https://developer.pebble.com/guides/events-and-services/accelerometer/
UP_VECTOR = np.array([0, 0, 1])
DOWN_VECTOR = np.array([0, 0, -1])
RIGHT_VECTOR = np.array([0, 1, 0])
LEFT_VECTOR = np.array([0, -1, 0])
FORWARD_VECTOR = np.array([1, 0, 0])
BACK_VECTOR = np.array([-1, 0, 0])

def save_coordinate_to_npy(x, y, z):
    if os.path.exists(STREAM_PATH):
        stream = np.load(STREAM_PATH)
        stream.append([x, y, z])
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

def cosineSimilarity(vectorA, vectorB):
    dotProduct = 0.0
    normA = 0.0
    normB = 0.0
    for i, vect in enumerate(vectorA):
        dotProduct += vectorA[i] * vectorB[i]
        normA += vectorA[i]**2
        normB += vectorB[i]**2

    return dotProduct / (math.sqrt(normA) * math.sqrt(normB))


def classify_action(accelVector):
    probableAction = RIGHT_ACTION
    cosineSim = -1.0

    if cosineSim < cosineSimilarity(accelVector,
                                           RIGHT_VECTOR):
        probableAction = RIGHT_ACTION

    if cosineSim < cosineSimilarity(accelVector, LEFT_VECTOR):
        probableAction = LEFT_ACTION

    if cosineSim < cosineSimilarity(accelVector, UP_VECTOR):
        probableAction = UP_ACTION

    if cosineSim < cosineSimilarity(accelVector, DOWN_VECTOR):
        probableAction = DOWN_ACTION

    if cosineSim < cosineSimilarity(accelVector, FORWARD_VECTOR):
        probableAction = FORWARD_ACTION

    if cosineSim < cosineSimilarity(accelVector, DOWN_VECTOR):
        probableAction = DOWN_ACTION

    return np.array([probableAction])