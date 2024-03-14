# CONCENTRATOR INTERFACE

## Installation

On Linux, if tkinter is not installed from below, run the following command :

```shell
sudo apt install python3-tk
```

## Using the interface

### START THE INTERFACE

First, open a terminal in the directory of the interface. You can start the program with this following commands :

#### Linux

```shell
./script_interface.py
```
or
```shell
python3 ./script_interface.py
```

#### Windows

```powershell
python .\script_interface.py
```

### INITIALIZATION OF THE INTERFACE

The initialization window is the first page you will see at the program start. It allow the user to choose which concentrator board is controlled. There are 3 tabs, each for a different initialization method.

#### Start by saved configuration

You can start the interface with a saved configuration. Select the wanted concentrator and start the interface. You can verify the configuration with the informations display under the concentrator choice.

#### Start by ID

You can start the interface with the concentrator ID. The programme will automatically calculate the IP address with the following rule :
- UCP IP : `10.3.171.ID:60002`
- TCP IP : `10.3.171.100+ID:7`

When you enter an ID, the programm show the calculate IPs before in the information field below the cincentrator number. If the configuration is good, you can start the interface.

#### Start by custom configuration

You can start the interface with a custom configuration. You can enter each parameter of the IP configuration. Then you can start the interface, with or without sending the gateway MAC address.

With the button `SAVE` you can add this configuration to the saved IP configuration (used in the first tab).

#### For all methods

If you check the *"Disable all channels at startup"* option, the programme send a command at the start of the interface to disabled all the channels.

**/!\ When you start the interface, a log file is created. (when you close the interface, it is compressed)**

### NAVIGATION THROUGH THE INTERFACE

The header of the interface show important information about the concentrator board (IP address, links status).

![Refresh buttons](graphics/refresh.png) : buttons to test the TCP or UDP links

`READ COUNTERS` : print via USB the status of 4 FIFOS associated with each ROB channel.

`RESET PULSE` : reset for RX/TX FIFOs in the ROB communication channels.

![Send button](graphics/send.png) : open custom packets window

`STOP` : stop the interface

A navigation bar allow the user to select the current page. The pages available are :

- `ROBS` : the configuration page of the ROBs
- `CB` : the configuration page of CB
- `ACQUISITION` : the configuration page of the acquisition
- `INTERFACE` : the configuration page of the interface

### ROBS CONFIGURATION

A page allow the user to configure all the ROBs connected to the CB. The page show the boards, with a color code corresponding to the state of each ROB :

![Green](graphics/ROB_green.png) : All good

![Blue](graphics/ROB_blue.png) : card with high voltage activated

![Grey](graphics/ROB_grey.png) : disabled card

![Yellow](graphics/ROB_yellow.png) : card in error

Next to each ROB picture, there is 3 buttons :

![Disable](graphics/desact.png) : disable the channel

![IO delay](graphics/io.png) : IO delay configuration

![Configuration](graphics/conf.png) : open the ROB configuration window

In the top, there are 5 buttons which act on all ROBs :

![Refresh](graphics/refresh.png) : refresh ROBs states. It send dummy word command to the enabled ROBs to know if they are in error.

![IO delay](graphics/global_io.png) : global IO delay. It configure the IO delay of each enabled card one after the other.

![Configuration](graphics/allConf.png) : open the window of the configuration of all the ROBs

`ENABLE ALL` : enable all the channels

`DISABLE ALL` : disable all the channels

### CB CONFIGURATION

#### FPGA section :

This section allow the user to reset and test the FPGAs.

![Reset](graphics/refresh.png) : reset the FPGAs. Yellow to reset with TCP connection and Blue with UDP connection.

![Write](graphics/send.png) & ![Read](graphics/receive.png) : write and read word with one of the link.

#### Serial section :

This section allow the user to use the serial connection between the ULTRASCALE FPGA and the SPARTAN 6 one. The commands are send to the ULTRASCALE and are transferred to the SPARTAN 6. It is the same command as the UART connection to the SPARTAN 6.

#### Advanced section :

You can display the advanced settings by check the advanced mode button.

Here you can flash the Ultrascale and Spartan 6 FPGAs. You can also get and set registers on the concentrator (index and values can be maximum 0xFFFFFFFF).


### ACQUISITION CONFIGURATION

#### Acquisition control :

The user can choose between a continuous acquisition or one with a specific number of events.

`LAUNCH` and `STOP` buttons can be used to start and stop the acquisition on all the activated ROBs.

A frame show the states of the 16 ROBs. The colors correspondence is the same as the ROBs page :
- Green : All good
- Blue : card with high voltage activated 
- Grey : disabled card
- Yellow : card in error

![Refresh](graphics/refresh.png) : This button allow the user to refresh the state of the ROBs.

Below this frame, there is a field used to display the information of the last time when an acquisition was start or stop on this interface.

/!\ This doesn't inform if an acquisition on the same CB was start or stop with an other interface.

#### DAQ server configuration

This section allow the user to set up the IP address of the DAQ server. It also possible to get the current address store on the CB.

There is also button to connect the CB to the set server.

/!\ At the moment it is not confirmed that the disconnect command works, so it has been disabled.

#### Acquisition configuration

This section can be used to configure the triggers.

The user can configure the L1 trigger and send the configuration to the CB with the button `CONFIG L1`.

The button `FORCE L2` activate the bypass of the L2 trigger.

The mask to disable the coming time-stamps can be configure in this section. It allow to ignore time-stamps from some or all the channels. The user can disable or enable all the channels, and then, he has to send this configuration with the button `SET TS MASK`.

__In the advanced mode :__

Each channel of the time-stamps mask can be set independantely. After set the wanted mask, the user can send it with the button `SET TS MASK`.

The user can also set the concentrator to keep all the time-stamps by checking the button corresponding, and then click `SET` in the side.

### INTERFACE CONFIGURATION

There is 3 sections.

#### Command configuration

The timeout of the two links can set in this section. /!\ It is the value for the interface (not the concentrator).

#### Interface parameters

Silent mode : When the silent mode is enabled, only important information are printed in the terminal

#### Other controls

The user can return to the initialization window with the button `RESTART` (he have to close all the top windows).

The field with the `LOG` button can be used to create a manual log. Enter the text of the log and click the button. This can be used when when you are about to make an important action.

### ROB CONFIGURATION WINDOW

#### Header

The header of the windows contain command to speed up the configuration of the ROBs.
- **To load a saved configuration** : seach for the configuration file (for example `conf_robs.json`) and load it . The button `LOAD` will only put the values into the entries of the windows.
- **To set all the values in the entries** : use  the button `SET ALL`. All the entries used to set a value need to be filled.
- **To read all the values** :  use  the button `READ ALL`.
- **To toggle in advanced mode** : use the checkbox

#### Buttons

![Write](graphics/write.png) : this button represent a data coming from the ROB.

![Read](graphics/read.png) : this button represent a data send by the GUI to the ROB.

In both case, a command is send to get or set the value.

#### Frames

The ROB configuration Window have 5 frames :

- `Card status` : This section allow the user to check the status of the board, like the version of the firmware or the temperature.
- `Acquisition parameters` : This section allow the user to configure the acquisition on the ROB and get some values.
- `MAROC slow-control` : This section allow the user to select a MAROC slow-control file, send it or open it.
- `High voltage` : This section allow the user to configure the high voltage parameters on the ROB.
- `Advanced` (only in advanced mode) : This section allow the user to access to advanced functionalities like writing and reading register or open the window to flash the ROB and FEB FPGA.

### MAROC SLOW-CONTROL

The MAROC slow-control window configuration can be open with the button `OPEN SC CONFIGURATION`. In this window, you can set the DAC 0 value, the OR mask and the channels gains.

The current file load, there are the current file loaded. In the files section, there are the following buttons :
- `RELOAD` : reload the current file by resetting the values.
- `LOAD` : load a file and display it's values.
- `SAVE` : save the changement in the current file.
- `BACKUP` : save the changement in an other choosen file.

When you make a backup, you can directly switch to it by checking `Switch to backup`.

### ROB AND FEB FPGA FLASH WINDOW

This window allow the user to access the function linked to the flash of the FPGA. It is accessible from the ROB configuration window.

The two buttons at the top are used to choose which FPGA you want to work on. The ROB FPGA is the Cyclone 5 and the FEB FPGA is the Spartan 6.

The second section, `FLASH`, allow the user to flash the chosen FPGA on the board.

The last section, `READ` which is only display on individual ROB control, is used to read and save the content of the board memory.

#### To flash the FPGA :

1) First, choose the board you want to flash.
2) Then find the transformed firmware file to fill up the path (corresponding to the selected board).
3) Finally, flash the board with the button `FLASH`.

#### To read the memory :

1) First, choose the board you want to read the memory.
2) Then start the reading with the button `READ`.
3) Finally, save the data with the button `SAVE`.

/!\ For now it will take a very long time.

### CUSTOM PACKETS SENDING

In the main header, there is a button to open the window to send customs commands. ![Send button](graphics/send.png)

The user can fill the field with desired values. Initially, there is 3 fields : the destination, the command and the size.

The user can add more data field to the packet and fill them. The size of the packet will update automatically.

#### To send custom packets :
1) First, choose the link with which you want to send the packet.
2) Then, fill up the fields.
3) Finally, send the packet with the button `SEND`.

### CONFIGURATION FILES

#### Configuration of the concentrator boards

The file `cbs_ip_saved_confs.json` contain the configuration of the concentrators used.

In this configuration file, there are the following parameters :

- UDP IP address
- UDP port
- TCP IP address
- TCP port
- IP mask
- Default gateway MAC address
- Information about the CB

#### Configuration of the read out boards

The file `conf_robs.json` contain the default configuration values of the ROBs. In this file, there are the following parameters :

- Acquisition mode
- TRT duration
- OR threshold level
- LED bias level
- Cable delay
- Hold delay
- High voltage value
- High voltage current value

#### Slow control of the MAROC

The file `dump_config_bits.txt` contain the MAROC slow control value of each bit. This slow control can be send into the ROBs configuration window.

## Methods of use

TO BE COMPLETED

## Troubleshooting

TO BE COMPLETED

## Program structure

The GUI program is composed by this Python scripts :

- `script_interface.py` : it is the script that load the CB configurations and call the methods to start the interface.
- `windows_def.py` : it is the script where all the window objects are declared.
- `graphics_objects.py` : it is the script where some particulars and big objects for the interface windows are declared.
- `functions_cb.py` : it is the script with the methods about the CB. For example about the network communication.
- `variables_cb.py` : it is the script containing the variables about the CB, like the command headers.
- `functions_interface.py` : it is the script with the methods about the interface.
- `variables_interface.py` : it is the script containing the variables for the interface.

The folder `configs` contain the saved configuration files.

The folder `firmware` contain the firmware files of the FPGAs.

The folder `graphics` contain the images used for the interface.

The folder `logs` contain the logs. **/!\ Each time the interface start a new log file is created. So at a moment, you need to delete the useless log files.**

