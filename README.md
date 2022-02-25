# e2-scripts

Scripts for dealing with electribe2 files.

Support:
http://www.korgforums.com/forum/phpBB2/viewtopic.php?p=769727#769727

e2all2pat.py  - Converts allpat file to a directory of e2pat files.  

e2pat2syx.py - Converts a pattern file in e2pat format to a pattern file in sysex format.

e2syx2pat.py - Converts a pattern file in sysex format to pattern file in e2pat format.

e2seqrot.py - Rotates sequence of specified part by specified number of steps.  Takes e2pat as input.

e2pat2all.py - Create allpatterns from a single pattern.

e2ev.py - Split event recording by pattern, create stems, mute parts, extract and replace patterns.

e2sysex.py - Communicate with electribe 2 via SysEx

e2-header.py - Edit file header to load sampler firmware on synth hardware

e2-init-pat.py - Insert custom init pattern in electribe 2 sampler firmware version 2.02

e2_syx_codec.py - Encode/Decode bytes to and from electribe SysEx format


## Example Usage

Print info on patterns found in file.e2ev:
```
python e2ev.py file.e2ev -i
```


Split a multi pattern event recording into multiple single pattern event recordings:
```
python e2ev.py file.e2ev -s
```


Create a stem event recording consisting of parts 1, 5 and 16 named 'drums':
```
python e2ev.py file.e2ev -c 0 4 15 -n drums
```
This will create file_drums_stem.e2ev



Mute channel 16 of the event recording:
```
python e2ev.py file.e2ev -m 15
```
This will overwrite the original file.e2ev



Extract all patterns files found in file.e2ev:
```
python e2ev.py file.e2ev -e
```
Patterns will be saved as file_pat_x.e2pat



Replace the second pattern of file.e2ev with pattern.e2pat:
```
python e2ev.py file.e2ev -r 1 -p pattern.e2pat
```

### Extra information

More information about the event recording format can be [found here](event-recording-notes.txt).