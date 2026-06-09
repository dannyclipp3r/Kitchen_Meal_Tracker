# Raspberry Pi 3 Touchscreen Setup

This app can run on a Raspberry Pi 3 with a touchscreen because the CustomTkinter UI uses normal click/tap controls. A touchscreen tap behaves like a mouse click, so the Back buttons do not need special code beyond being large enough to tap.

## What You Need

### Hardware

- Raspberry Pi 3
- MicroSD card with Raspberry Pi OS Desktop installed
- Official Raspberry Pi touchscreen or HDMI touchscreen
- Keyboard/mouse for first-time setup
- Reliable 5V power supply

### System Packages

Run this on the Raspberry Pi:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-tk
```

### Python Package

From the project folder:

```bash
pip3 install -r requirements.txt
```

`requirements.txt` should include:

```text
customtkinter>=5.2.2
```

## Run The Touch UI

```bash
cd ~/Kitchen\ Meal\ Tracker
python3 custom_ui.py
```

## Touchscreen Back Behavior

The ingredient screen already has touchscreen-friendly Back controls:

- `Back` under the ingredient edit buttons
- bottom `Back`
- bottom `Close`

For Raspberry Pi touchscreen use, prefer the visible `Back` button in the right-side ingredient panel. It returns to the previous page, such as Check Meals or Generate Meal Plan.

## Optional Fullscreen Mode

For kiosk-style touchscreen use, you can add this inside `KitchenMealTrackerApp.__init__` in `custom_ui.py`:

```python
self.attributes("-fullscreen", True)
```

To exit fullscreen from code later, bind Escape:

```python
self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
```

## Optional Physical Back Button

If you later want a physical hardware Back button wired to GPIO, install:

```bash
pip3 install gpiozero
```

Then you can wire a push button to a GPIO pin and call the same screen function used by the UI Back button. This is optional; it is not needed for touchscreen tapping.
