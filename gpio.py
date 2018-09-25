from RPi import GPIO

class PullUpPin(object):
    def __init__(self, pin_number, update_callback):
        self.pin_number = pin_number
        self.update_callback = update_callback

        GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pin_state = GPIO.input(pin_number)

        GPIO.add_event_detect(pin_number, GPIO.BOTH)
        GPIO.add_event_callback(pin_number, self.handle_event)

    def handle_event(self, _):
        new_state = GPIO.input(self.pin_number)
        if new_state != self.pin_state:
            self.pin_state = new_state
            self.update_callback(new_state)


class Toggle(object):
    def __init__(self, pin_number, toggle_callback):
        self.pin = PullUpPin(pin_number, self.handle_pin_update)
        self.initial_pin_state = self.pin.pin_state
        self.toggle_callback = toggle_callback

    def handle_pin_update(self, new_state):
        if new_state == self.initial_pin_state:
            self.toggle_callback()


class TurnState(object):
    IDLE = 0
    CW = 1
    CCW = 2


class RotaryEncoder(object):
    def __init__(self, pin_a_number, pin_b_number, turn_callback):
        self.pin_a = PullUpPin(pin_a_number, self.handle_event_pin_a)
        self.pin_b = PullUpPin(pin_b_number, self.handle_event_pin_b)
        self.turn_callback = turn_callback
        self.turn_state = TurnState.IDLE

    def handle_event_pin_a(self, pin_a_state):
        self.handle_state_event('a', pin_a_state)

    def handle_event_pin_b(self, pin_b_state):
        self.handle_state_event('b', pin_b_state)

    def handle_state_event(self, pin, new_pin_state):
        old_turn_state = self.turn_state

        new_turn_state = {
            (TurnState.IDLE, 'a', 0): TurnState.CCW,
            (TurnState.IDLE, 'b', 0): TurnState.CW,
            (TurnState.CW,   'a', 0): TurnState.CW,
            (TurnState.CW,   'b', 1): TurnState.CW,
            (TurnState.CW,   'a', 1): TurnState.IDLE,
            (TurnState.CCW,  'b', 0): TurnState.CCW,
            (TurnState.CCW,  'a', 1): TurnState.CCW,
            (TurnState.CCW,  'b', 1): TurnState.IDLE,
        }.get((old_turn_state, pin, new_pin_state), old_turn_state)

        self.turn_state = new_turn_state

        if old_turn_state != TurnState.IDLE and new_turn_state == TurnState.IDLE:
            self.turn_callback(old_turn_state == TurnState.CW)
