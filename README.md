<br />
<div align="center">
    <img src="assets/logo1.png" alt="Logo" width="80" height="80">

<h3 align="center">Linux Capture-The-Flag Game</h3>

  <p align="center">
    Introduction CTF Python Game for new students
    Basic Linux Commands (pwd, ls, cat)
    <br />
  </p>
</div>

## GUI

![Product Name Screen Shot][product-screenshot]

### Built With

* [![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
* [![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green)](https://docs.python.org/3/library/tkinter.html)

<!-- GETTING STARTED -->
## Getting Started

Download whole repo to find all the hidden flags within. 
To start the application, run A3testgui5.py file.

### Prerequisites

* python3 *atleast 3.13.2*
  ```sh
  python3 --version
  ```

### Installation

### If connected to internet
1. Clone the repo
   ```sh
   git clone https://github.com/awdpar/linux-ctf.git
   ```
2. Navigate to folder
   ```sh
   [~/linux-ctf/A3]
   ```
3. Run the game
   ```sh
   python3 A3testgui5.py
   ```

### If no internet
1. Download git repo zip to flash drive
  ```sh
  https://github.com/awdpar/linux-ctf.git
  ```
2. Locate folder on USB in linux and copy over linux-ctf-main into pc directory

3. Right click on folder and click "open terminal here" & you should be in the ctf directory in terminal

4. Run update 
  ```sh
  sudo apt update
  ```

5. Install Tkinter
  ```sh
  sudo apt install python3-tk
  ```

6. Run the game
   ```sh
   python3 A3testgui5.py
   ```

## Adding more questions

To add more questions after the fact, 

Add your question/flag/difficulty in
   ```sh
   A3 -> questions.json
   ```

Then add a new file with the code for the question in
   ```sh
   A3 -> questions folder
   ```

[product-screenshot]: assets/currentSS.png