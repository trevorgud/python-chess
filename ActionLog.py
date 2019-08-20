class ActionLog:
  def __init__(self, time, msg):
    self.time = time
    self.msg = msg

  def __str__(self):
    return self.time.strftime("%H:%M:%S") + " " + self.msg
