from threading import Timer


class PerpetualAlternatedTimer:
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, seconds_alt, target, target_alt):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.seconds_alt = seconds_alt
        self.target = target
        self.target_alt = target_alt
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer_alt()

    def _handle_target_alt(self):
        self.is_running = True
        self.target_alt()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        # Code could have been running when cancel was called.
        if self._should_continue:
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def _start_timer_alt(self):
        # Code could have been running when cancel was called.
        if self._should_continue:
            self.thread = Timer(self.seconds_alt, self._handle_target_alt)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()

    def cancel(self):
        if self.thread is not None:
            # Just in case thread is running and cancel fails.
            self._should_continue = False
            self.thread.cancel()
