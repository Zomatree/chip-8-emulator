from . import CPU, Display
import configparser
import sys

config = configparser.ConfigParser()
config.read('config.ini')

if config["logging"]["level"] != "None":
    import logging
    logging.basicConfig(level=getattr(logging, config["logging"]["level"]))

display = Display(16, config["input"])
cpu = CPU(display)
cpu.load_program(f"{config['rom']['folder']}{sys.argv[1]}")

cpu.mainloop()
