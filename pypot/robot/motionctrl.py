import threading
import time

class PoseMotionController(threading.Thread):
    """Class for simple pose motion controller."""
     
    def __init__(self, motor, tf, freq = 10):
        """Initialization
        
        :param motor  the Motor instance to apply the motion to.
        :param tf     timed function whose values will update the
                      goal_position of the motor. 
        """
        threading.Thread.__init__(self)
        
        self.daemon = True # don't block main program
        self.name = 'posemotion-{}'.format(thread.get_ident())
    
        self._alive = True # change to false to kill the motion
        self._suspended = False
        self._suspendlock = threading.Lock()
        self._suspendtime = 0.0
        self._zero  = time.time()
        
        self.motor = motor
        self.tf    = tf
        self.freq  = freq
        
    def update(self, elapsed):
        """Update motor values"""
        goalpos = self.tf.get_value(elapsed)
        self.motor.goal_position = goalpos
        
        
    def run(self):
        self._zero = time.time()
        while self._alive:
            t1 = time.time()
            elapsed = t1 - self._zero
            
            self.update(elapsed)
            
            if self.tf.has_finished(elapsed):
                self._alive = False
                break;
                       
            time.sleep(1.0 / self.freq - (time.time() - t1))

            self._suspendlock.acquire()
            self._suspendlock.release()         
    
    def stop(self):
        """Stop the motion, stop the thread."""
        self._alive = False
        self.resume()

    # Suspending motion
    
    @property
    def suspended(self):
        return self._suspended
    
    def suspend(self):
        """Suspend the motion. 
        Can be called on already supsended motion without effect
        """
        if not self._suspended:
            self._suspendtime = time.time()
            self._supended = True
            self._suspendlock.acquire()
        
    def resume(self):
        """Resume the motion. 
        Can be called on running motion without effect.
        """
        if self._suspended:
            self._supended = False
            self._zero = time.time() - self._suspendtime
            self._suspendlock.release()            

class PoseSpeedTorqueController(PoseMotionController):
    """Class for pose, speed and torque motion controller."""
    
    def __init__(self, motor, tripletf, freq = 10):
        PoseMotionController.__init__(self, motor, tripletf, freq = freq)
        
    def update(self, elapsed):
        goalpos, maxspeed, torquelim = self.tf.get_value(elapsed)
        if goalpos is not None:
            self.motor.goal_position = goalpos
        if maxspeed is not None:
            self.motor.moving_speed  = maxspeed
        if torquelim is not None:
            self.motor.torque_lim    = torquelim
        