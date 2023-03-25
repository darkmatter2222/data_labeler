import sys, os, signal

sys.path.append(os.path.realpath('..'))

from interface import bbox_label

main_interface = bbox_label()
main_interface.start()

