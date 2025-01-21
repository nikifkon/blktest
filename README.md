
# Description

Run fio randread and randwrite tests agains `FILENAME`. Draw bar chart for mean latecy depending on iodepth and save it to `OUTPUT`

# Usage

```
python3 blktest.py [-h] -n NAME -f FILENAME -o OUTPUT [-d IODEPTH [IODEPTH ...]]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME
  -f FILENAME, --filename FILENAME
  -o OUTPUT, --output OUTPUT
  -d IODEPTH [IODEPTH ...], --iodepth IODEPTH [IODEPTH ...]
```