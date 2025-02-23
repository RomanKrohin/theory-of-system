import transitions
from transitions import Machine
import time

class WashingMachine(object):
    pass

states = ["waiting", "washing", "rinsing", "spinning", "finished", "fault", "stopped"]

transition_table = [
    { 'trigger': 'start_button', 'source': 'waiting', 'dest': 'washing' },
    { 'trigger': 'washing_done', 'source': 'washing', 'dest': 'rinsing' },
    { 'trigger': 'rinsing_done', 'source': 'rinsing', 'dest': 'spinning' },
    { 'trigger': 'spinning_done', 'source': 'spinning', 'dest': 'finished' },
    { 'trigger': 'error', 'source': '*', 'dest': 'fault' },
    { 'trigger': 'reset', 'source': 'finished', 'dest': 'waiting' },
    { 'trigger': 'repair', 'source': 'fault', 'dest': 'stopped' },
    { 'trigger': 'power_off', 'source': '*', 'dest': 'stopped' },
    { 'trigger': 'power_on', 'source': 'stopped', 'dest': 'waiting' }
]

washing_machine = WashingMachine()
fsm = Machine(washing_machine, states=states, transitions=transition_table, initial="waiting")

def wash() -> None:
    time.sleep(5)
    if not washing_machine.is_fault():
        washing_machine.washing_done()
        print("Стирка завершена, переход к полосканию.")
    else:
        washing_machine.error()
        print("Ошибка стирки! Стиральная машина неисправна.")

def rinse() -> None:
    time.sleep(3)
    if not washing_machine.is_fault():
        washing_machine.rinsing_done()
        print("Полоскание завершено, переход к отжиму.")
    else:
        washing_machine.error()
        print("Ошибка полоскания! Стиральная машина неисправна.")

def spin() -> None:
    time.sleep(4)
    if not washing_machine.is_fault():
        washing_machine.spinning_done()
        print("Отжим завершен, стирка завершена.")
    else:
        washing_machine.error()
        print("Ошибка отжима! Стиральная машина неисправна.")

def press_start_button() -> None:
    if washing_machine.is_fault():
        print("Стиральная машина неисправна, запуск невозможен до ремонта.")
        return
    washing_machine.start_button()
    print("Стиральная машина начала стирку.")

def reset_washing_machine() -> None:
    if washing_machine.is_finished():
        washing_machine.reset()
        print("Стиральная машина готова к новому использованию.")
    else:
        print("Сброс невозможен: стиральная машина не в состоянии 'завершено'.")

# Пример симуляции
press_start_button()
wash()
rinse()
spin()
reset_washing_machine()