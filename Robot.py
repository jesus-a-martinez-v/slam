import random


# This robot lives in 2D, x-y space, and its motion is
# pointed in a random direction, initially.
# It moves in a straight line until it comes close to a wall
# at which point it stops.
#
# For measurements, it  senses the x- and y-distance
# to landmarks. This is different from range and bearing as
# commonly studied in the literature, but this makes it much
# easier to implement the essentials of SLAM without
# cluttered math.
class Robot:
    def __init__(self, world_size=100.0, measurement_range=30.0,
                 motion_noise=1.0, measurement_noise=1.0):
        """
        Creates a robot with the specified parameters and initializes
        the location (self.x, self.y) to the center of the world
        :param world_size: World size along each dimension.
        :param measurement_range: The max distance the robot is able to sense along each axis.
        :param motion_noise: Motion sensor noise.
        :param measurement_noise: Measurement sensor noise.
        """
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.landmarks = []
        self.num_landmarks = 0

    # returns a positive, random float
    def _rand(self):
        return random.random() * 2.0 - 1.0

    # --------
    # move: attempts to move robot by dx, dy. If outside world
    #       boundary, then the move does nothing and instead returns failure
    #
    def move(self, dx, dy):
        """
        Attempts to move robot by dx, dy. If outside world
        boundary, then the move does nothing and instead returns failure
        :param dx: x-axis delta.
        :param dy: y-axis delta.
        :return: True if the robot were able to move, False otherwise.
        """
        x = self.x + dx + (self._rand() * self.motion_noise)
        y = self.y + dy + (self._rand() * self.motion_noise)

        if (x < 0.0 or x > self.world_size) or (y < 0.0 or y > self.world_size):
            return False
        else:
            self.x = x
            self.y = y
            return True

    def sense(self):
        """
        This function does not take in any parameters, instead it references internal variables
        (such as self.landmarks) to measure the distance between the robot and any landmarks
        that the robot can see (that are within its measurement range).
        This function returns a list of landmark indices, and the measured distances (dx, dy) between the robot's
        position and said landmarks.
        One item in the returned list should be in the form: [landmark_index, dx, dy].
        """
        all_landmarks_within_range = self.measurement_range == -1
        measurements = []

        for index, (landmark_x, landmark_y) in enumerate(self.landmarks):
            dx = (landmark_x - self.x) + (self._rand() * self.measurement_noise)
            dy = (landmark_y - self.y) + (self._rand() * self.measurement_noise)

            is_landmark_within_range = (all_landmarks_within_range or
                                        (abs(dx) <= self.measurement_range) and
                                        (abs(dy) <= self.measurement_range))

            if is_landmark_within_range:
                measurements.append([index, dx, dy])

        return measurements

    def make_landmarks(self, num_landmarks):
        """
        Makes random landmarks located in the world.
        :param num_landmarks: Number of landmarks to randomly place in the world.
        """
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append([round(random.random() * self.world_size),
                                   round(random.random() * self.world_size)])
        self.num_landmarks = num_landmarks

    # called when print(robot) is called; prints the robot's location
    def __repr__(self):
        return 'Robot: [x=%.5f y=%.5f]' % (self.x, self.y)
