<p align="center">
  <img src="https://cloud.mcjkula.com/index.php/apps/files_sharing/publicpreview/kcsyNFswBZAGCe6?file=/&fileId=87204&x=3600&y=2338&a=true" alt="Time Dilation Calculator" width="auto" height="auto">
</p>

# Time Dilation Calculator

This repository contains a Time Dilation Calculator built with `Flet`. It allows users to input a velocity and calculate the lorentz-factor and dilated time based on the given proper time.

## Technologies Used

- Framework: [flet](https://github.com/flet-dev/flet) (Flet enables developers to easily build realtime web, mobile and desktop apps in Python).

## Features

### Lorentz Factor Calculation
- Users can input the velocity of an object and the speed of light to calculate the lorentz-factor.
- Supports various units of velocity including km/s, % of c, m/s, and km/h.

### Time Dilation Calculation
- Calculates the dilated time based on the given proper time and the calculated lorentz-factor.
- Displays the lorentz-factor and dilated time.

### Lorentz Factor Visualization
- Visualizes the Lorentz Factor using the Phytagoras Theorem.
- Represents the typical Lorentz Factor/Time Dilation curve in a new way, to better see the current state of dilated time.

<p align="center">
  <img src="./output_centered.gif">
</p>

## Requirements

To run and use the Time Dilation Calculator, you need the following:

- `flet` framework installed.
- Python 3.10 (Because of the Match-Case)

## Usage

1. Clone this repository.
2. Ensure all requirements are met.
3. Run the script.

```bash
python main.py
```

## Future Plans
- Implement error handling for invalid input values.
- Provide additional information on lorentz-factor and time dilation within the app.
- ~~Include visualizations to better illustrate the concept of time dilation.~~ (Done)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. [Maciej Kula](https://github.com/mcjkula).
