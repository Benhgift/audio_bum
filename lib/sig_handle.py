import signal
import sys
from lib.helpers import close_streams


def setup_sig_handler(strms):
    def handler(signum, frame):
        close_streams([strms.into, strms.out])
        print('done')
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
