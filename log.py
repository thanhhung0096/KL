import logging
FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s' 
logging.basicConfig(filename='/home/pi/KL/FacialDetection/log/log',level=logging.DEBUG,format= FORMAT)

def _info(name):
    logging.info("Recognized user:  " +  name)
