

class Device:
    def __init__(self, usual_rspnd_time = 5, name = "default device"):
        # check if the number passed in is a digit, otherwise set to default value
        self.usual_rspnd_time = (usual_rspnd_time) if isdigit(usual_rspnd_time) else  5
        self.name = name


# here we defined a dict of the device names
# format: { service name: respond time}
names = {"SCE LED Sign": 5, "SCE TV": 5, "service name placeholder": 5}

# a variable to store the number of devices we have
num_devices = len(names)

status_dict = {}
status_gauges = []
#initialize the status dictionary
def initialize():
    global status_dict
    # set up gauges
    for name in names:
        status_dict.update(
            #{f"{name}": prometheus_client.Gauge(f"{name}",f"gauge for {name}")}
        )
    # get initial data
    for name in names:
        pass