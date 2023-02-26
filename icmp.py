from argparse import ArgumentParser, Namespace
from logging import info
from sys import argv, exit

from PyQt5.QtWidgets import QApplication

from icmpflood.gui.main_window import MainWindow
from icmpflood.flooder_runner import FlooderConsoleRunner




def launch_gui():
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec_())


def launch_cmd(cmd_options: Namespace):
    FlooderConsoleRunner(
        threads_number=cmd_options.threads,
        arguments={
            'ip': cmd_options.ip,
            'port': cmd_options.port,
            'length': cmd_options.length,
            'frequency': cmd_options.frequency
        }
    ).run()


if __name__ == "__main__":
    log_print()

    argument_parser = ArgumentParser(
        prog='ICMP-Flooder',
        usage='''python3 icmpflood.py { gui | cmd [options] }
                    There are two modes to use this simple application:
                    1. gui  - Allows to run application with GUI interface;
                    2. cmd  - Run application into terminal (print -h for more details).
            ''',
        description='''
                    There is simple python script that I implemented while studying at Lewis University.
                    The main goal of this project was to become familiar with  simple Python script that 
                    provides flooding ability by sending empty ICMP packets to a specified target by IP 
                    or URL address. This script also provides additional options to set packet length, 
                    frequency of sending generated ICMP packets,and number of threads. Enjoy! :)
            ''',
        add_help=True,
        allow_abbrev=True
    )

    sub_parser = argument_parser.add_subparsers(title='Script Modes', dest='mode', required=True)

    sub_parser.add_parser('gui', help='Allows you to run the application with a GUI interface.')
    cmd = sub_parser.add_parser('cmd', help='Run the application in the terminal (print -h for more details).')

    cmd.add_argument('-u', metavar='--url', help='Target URL address', required=False, type=str)
    cmd.add_argument('-i', metavar='--ip', help='Target IP address', required=True, type=str)
    cmd.add_argument('-p', metavar='--port', help='Target address port number (for IP address)',
                     required=False, choices=range(0, 65536), default=80, type=int)

    cmd.add_argument('-t', metavar='--threads', help='Number of threads', required=False, default=1, type=int)
    cmd.add_argument('-l', metavar='--length', help='Packet frame length', required=False, default=60, type=int)
    cmd.add_argument('-f', metavar='--frequency', help='Frequency of sending packets', required=False, default=0.1, type=float)

    arguments = argument_parser.parse_args()

    if arguments.mode == "gui":
        launch_gui()
    else:
        launch_cmd(arguments)
