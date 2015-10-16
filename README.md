# id_book

Simple program to manage a simple ID database utilising an RFID scanner which simulates a keyboard.

## Dependencies

This python3 program uses PyQt5.

On a Debian type system this should install dependencies:

```
$ sudo apt-get install python3-pyqt5 python-sqlite2
```

## Running

```
$ ./main.py
```
It will search for an asset folder which contains the database and any photographs.
Photographs should be 256x256 and can be created with imagemagick. These needn't be in the assets folder.

```
$ convert input_image -resize 256x256 output_img
```

Where input_image is the path to a photo such as /home/ali/Pictures/webcam/photo.jpg and output_img is the new file path such as ./assets/ali_00.jpg

You can install imagemagick like so on a GNU/Debian system

```
$ sudo apt-get install imagemagick
```

### To do

Allow for capturing webcam images and or converting them without installing imagemagick
