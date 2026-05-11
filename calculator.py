"""
╔══════════════════════════════════════════════╗
║         SMART CALCULATOR - Python Project    ║
║               1st Year Project               ║
╚══════════════════════════════════════════════╝

Features:
  - Basic arithmetic operations
  - Scientific functions (sqrt, power, log, trig)
  - Calculation history with memory recall
  - Unit converter (km↔miles, °C↔°F, kg↔lbs)
  - Expression evaluator
  - Error handling & input validation
"""

import math
import os
from datetime import datetime


# ─────────────────────────────────────────────
#  COLORS (for a nice terminal look)
# ─────────────────────────────────────────────
class Color:
    HEADER  = "\033[95m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"


# ─────────────────────────────────────────────
#  HISTORY MANAGER
# ─────────────────────────────────────────────
class History:
    def __init__(self):
        self._records = []

    def add(self, expression: str, result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._records.append({"time": timestamp, "expr": expression, "result": result})

    def show(self):
        if not self._records:
            print(f"{Color.YELLOW}  No history yet.{Color.RESET}")
            return
        print(f"\n{Color.CYAN}{'─'*50}")
        print(f"  {'#':<4} {'Time':<10} {'Expression':<22} Result")
        print(f"{'─'*50}{Color.RESET}")
        for i, rec in enumerate(self._records, 1):
            print(f"  {i:<4} {rec['time']:<10} {rec['expr']:<22} {Color.GREEN}{rec['result']}{Color.RESET}")
        print(f"{Color.CYAN}{'─'*50}{Color.RESET}")

    def last_result(self):
        if self._records:
            return self._records[-1]["result"]
        return None

    def clear(self):
        self._records.clear()
        print(f"{Color.YELLOW}  History cleared.{Color.RESET}")


# ─────────────────────────────────────────────
#  CALCULATOR CORE
# ─────────────────────────────────────────────
class Calculator:
    def __init__(self):
        self.history = History()
        self.memory  = 0.0          # M+ / MR / MC support

    # ── Basic Operations ──────────────────────
    def add(self, a, b):        return a + b
    def subtract(self, a, b):   return a - b
    def multiply(self, a, b):   return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        return a / b

    def modulus(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot mod by zero!")
        return a % b

    def integer_divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        return a // b

    # ── Scientific Operations ─────────────────
    def power(self, base, exp):     return base ** exp
    def square_root(self, n):
        if n < 0:
            raise ValueError("Cannot take square root of a negative number!")
        return math.sqrt(n)
    def cube_root(self, n):         return math.copysign(abs(n) ** (1/3), n)
    def log10(self, n):
        if n <= 0: raise ValueError("Logarithm undefined for non-positive numbers!")
        return math.log10(n)
    def ln(self, n):
        if n <= 0: raise ValueError("Natural log undefined for non-positive numbers!")
        return math.log(n)
    def factorial(self, n):
        if n < 0 or n != int(n):
            raise ValueError("Factorial is only defined for non-negative integers!")
        return math.factorial(int(n))
    def sin_deg(self, deg):         return math.sin(math.radians(deg))
    def cos_deg(self, deg):         return math.cos(math.radians(deg))
    def tan_deg(self, deg):
        if deg % 180 == 90:
            raise ValueError("tan is undefined at 90°, 270°, ...")
        return math.tan(math.radians(deg))
    def absolute(self, n):          return abs(n)
    def reciprocal(self, n):
        if n == 0: raise ZeroDivisionError("Reciprocal of 0 is undefined!")
        return 1 / n
    def percent(self, n):           return n / 100

    # ── Unit Converter ────────────────────────
    CONVERSIONS = {
        "1": ("km  → miles",    lambda x: x * 0.621371),
        "2": ("miles → km",     lambda x: x * 1.60934),
        "3": ("°C  → °F",       lambda x: x * 9/5 + 32),
        "4": ("°F  → °C",       lambda x: (x - 32) * 5/9),
        "5": ("kg  → lbs",      lambda x: x * 2.20462),
        "6": ("lbs → kg",       lambda x: x / 2.20462),
        "7": ("m   → feet",     lambda x: x * 3.28084),
        "8": ("feet → m",       lambda x: x / 3.28084),
        "9": ("litres → gal",   lambda x: x * 0.264172),
        "10":("gal → litres",   lambda x: x / 0.264172),
    }


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"""{Color.CYAN}{Color.BOLD}
  ╔══════════════════════════════════════════╗
  ║        🧮  SMART CALCULATOR  🧮          ║
  ║           1st Year Python Project        ║
  ╚══════════════════════════════════════════╝{Color.RESET}""")

def get_number(prompt="  Enter number: "):
    while True:
        try:
            return float(input(f"{Color.YELLOW}{prompt}{Color.RESET}"))
        except ValueError:
            print(f"{Color.RED}  ✗ Invalid input. Please enter a valid number.{Color.RESET}")

def show_result(expr: str, result, calc: Calculator):
    rounded = round(result, 10) if isinstance(result, float) else result
    print(f"\n  {Color.GREEN}✔  {expr} = {Color.BOLD}{rounded}{Color.RESET}")
    calc.history.add(expr, rounded)

def pause():
    input(f"\n{Color.BLUE}  Press Enter to continue...{Color.RESET}")


# ─────────────────────────────────────────────
#  MENUS
# ─────────────────────────────────────────────
MAIN_MENU = f"""
{Color.BOLD}  ┌─────────────────────────────────────┐
  │           SELECT CATEGORY           │
  ├─────────────────────────────────────┤
  │  1. Basic Arithmetic                │
  │  2. Scientific Functions            │
  │  3. Unit Converter                  │
  │  4. Expression Evaluator            │
  │  5. View History                    │
  │  6. Memory Operations               │
  │  0. Exit                            │
  └─────────────────────────────────────┘{Color.RESET}"""

BASIC_MENU = f"""
{Color.BOLD}  ── BASIC ARITHMETIC ──────────────────
  1. Addition          ( a + b )
  2. Subtraction       ( a - b )
  3. Multiplication    ( a × b )
  4. Division          ( a ÷ b )
  5. Modulus / Remainder ( a % b )
  6. Integer Division  ( a // b )
  0. Back{Color.RESET}"""

SCI_MENU = f"""
{Color.BOLD}  ── SCIENTIFIC FUNCTIONS ──────────────
  1.  Power            ( a ^ b )
  2.  Square Root      ( √n )
  3.  Cube Root        ( ∛n )
  4.  log₁₀(n)
  5.  ln(n)  (natural log)
  6.  Factorial        ( n! )
  7.  sin(°)
  8.  cos(°)
  9.  tan(°)
  10. Absolute value   ( |n| )
  11. Reciprocal       ( 1/n )
  12. Percentage       ( n% )
  0.  Back{Color.RESET}"""


# ─────────────────────────────────────────────
#  SECTION HANDLERS
# ─────────────────────────────────────────────
def basic_section(calc: Calculator):
    while True:
        print(BASIC_MENU)
        choice = input(f"{Color.CYAN}  Choice: {Color.RESET}").strip()
        if choice == "0":
            break

        ops = {
            "1": ("+",   calc.add),
            "2": ("-",   calc.subtract),
            "3": ("×",   calc.multiply),
            "4": ("÷",   calc.divide),
            "5": ("%",   calc.modulus),
            "6": ("//",  calc.integer_divide),
        }
        if choice in ops:
            sym, fn = ops[choice]
            a = get_number("  Enter first number : ")
            b = get_number("  Enter second number: ")
            try:
                result = fn(a, b)
                show_result(f"{a} {sym} {b}", result, calc)
            except (ZeroDivisionError, ValueError) as e:
                print(f"{Color.RED}  ✗ Error: {e}{Color.RESET}")
        else:
            print(f"{Color.RED}  ✗ Invalid choice.{Color.RESET}")
        pause()


def scientific_section(calc: Calculator):
    while True:
        print(SCI_MENU)
        choice = input(f"{Color.CYAN}  Choice: {Color.RESET}").strip()
        if choice == "0":
            break

        try:
            if choice == "1":
                a = get_number("  Base  : ")
                b = get_number("  Exponent: ")
                show_result(f"{a}^{b}", calc.power(a, b), calc)
            elif choice == "2":
                n = get_number("  Enter n: ")
                show_result(f"√({n})", calc.square_root(n), calc)
            elif choice == "3":
                n = get_number("  Enter n: ")
                show_result(f"∛({n})", calc.cube_root(n), calc)
            elif choice == "4":
                n = get_number("  Enter n: ")
                show_result(f"log₁₀({n})", calc.log10(n), calc)
            elif choice == "5":
                n = get_number("  Enter n: ")
                show_result(f"ln({n})", calc.ln(n), calc)
            elif choice == "6":
                n = get_number("  Enter n: ")
                show_result(f"{int(n)}!", calc.factorial(n), calc)
            elif choice == "7":
                d = get_number("  Angle (degrees): ")
                show_result(f"sin({d}°)", calc.sin_deg(d), calc)
            elif choice == "8":
                d = get_number("  Angle (degrees): ")
                show_result(f"cos({d}°)", calc.cos_deg(d), calc)
            elif choice == "9":
                d = get_number("  Angle (degrees): ")
                show_result(f"tan({d}°)", calc.tan_deg(d), calc)
            elif choice == "10":
                n = get_number("  Enter n: ")
                show_result(f"|{n}|", calc.absolute(n), calc)
            elif choice == "11":
                n = get_number("  Enter n: ")
                show_result(f"1/{n}", calc.reciprocal(n), calc)
            elif choice == "12":
                n = get_number("  Enter n: ")
                show_result(f"{n}%", calc.percent(n), calc)
            else:
                print(f"{Color.RED}  ✗ Invalid choice.{Color.RESET}")
                continue
        except (ZeroDivisionError, ValueError) as e:
            print(f"{Color.RED}  ✗ Error: {e}{Color.RESET}")
        pause()


def converter_section(calc: Calculator):
    while True:
        print(f"\n{Color.BOLD}  ── UNIT CONVERTER ──────────────────{Color.RESET}")
        for key, (label, _) in calc.CONVERSIONS.items():
            print(f"  {key:>2}. {label}")
        print(f"   0. Back")
        choice = input(f"{Color.CYAN}  Choice: {Color.RESET}").strip()
        if choice == "0":
            break
        if choice in calc.CONVERSIONS:
            label, fn = calc.CONVERSIONS[choice]
            val = get_number(f"  Enter value ({label.split('→')[0].strip()}): ")
            result = fn(val)
            show_result(f"{val} {label}", result, calc)
        else:
            print(f"{Color.RED}  ✗ Invalid choice.{Color.RESET}")
        pause()


def expression_section(calc: Calculator):
    """Safe expression evaluator using math namespace."""
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed["abs"] = abs
    last = calc.history.last_result()
    if last is not None:
        allowed["ans"] = last

    print(f"""
{Color.BOLD}  ── EXPRESSION EVALUATOR ──────────────
  Type a math expression and press Enter.
  Supported: +  -  *  /  **  //  %
             sqrt(n)  log10(n)  sin(n)  cos(n)  tan(n)
             pi  e  ans (last result)
  Type 'back' to return.{Color.RESET}""")

    while True:
        expr = input(f"\n{Color.YELLOW}  >> {Color.RESET}").strip()
        if expr.lower() == "back":
            break
        if not expr:
            continue
        try:
            result = eval(expr, {"__builtins__": {}}, allowed)  # sandboxed eval
            show_result(expr, result, calc)
            allowed["ans"] = result
        except ZeroDivisionError:
            print(f"{Color.RED}  ✗ Division by zero!{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}  ✗ Invalid expression: {e}{Color.RESET}")


def memory_section(calc: Calculator):
    print(f"\n{Color.BOLD}  ── MEMORY OPERATIONS ──────────────{Color.RESET}")
    print(f"  Current Memory: {Color.GREEN}{calc.memory}{Color.RESET}\n")
    print("  1. M+  (Add to memory)")
    print("  2. M-  (Subtract from memory)")
    print("  3. MR  (Recall memory)")
    print("  4. MC  (Clear memory)")
    print("  0. Back")
    choice = input(f"{Color.CYAN}  Choice: {Color.RESET}").strip()
    if choice == "1":
        val = get_number("  Value to add: ")
        calc.memory += val
        print(f"{Color.GREEN}  ✔ Memory updated → {calc.memory}{Color.RESET}")
    elif choice == "2":
        val = get_number("  Value to subtract: ")
        calc.memory -= val
        print(f"{Color.GREEN}  ✔ Memory updated → {calc.memory}{Color.RESET}")
    elif choice == "3":
        print(f"{Color.GREEN}  MR = {calc.memory}{Color.RESET}")
    elif choice == "4":
        calc.memory = 0.0
        print(f"{Color.YELLOW}  Memory cleared.{Color.RESET}")
    pause()


# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
def main():
    calc = Calculator()
    while True:
        clear()
        banner()
        print(MAIN_MENU)
        choice = input(f"{Color.CYAN}  Your choice: {Color.RESET}").strip()

        if choice == "1":
            basic_section(calc)
        elif choice == "2":
            scientific_section(calc)
        elif choice == "3":
            converter_section(calc)
        elif choice == "4":
            expression_section(calc)
        elif choice == "5":
            calc.history.show()
            ans = input(f"\n{Color.YELLOW}  Clear history? (y/n): {Color.RESET}").lower()
            if ans == "y":
                calc.history.clear()
            pause()
        elif choice == "6":
            memory_section(calc)
        elif choice == "0":
            print(f"\n{Color.GREEN}  Thank you for using Smart Calculator! Goodbye 👋{Color.RESET}\n")
            break
        else:
            print(f"{Color.RED}  ✗ Invalid choice. Please try again.{Color.RESET}")
            pause()


if __name__ == "__main__":
    main()
