# e2

Scripts for dealing with electribe2 files.

e2all2pat.py  - Converts allpat file to a directory of e2pat files.  

e2pat2syx.py - Converts a pattern file in e2pat format to a pattern file in sysex format.
                BUG - Creates sysex that dumps to channel 8.  
                Workaround - Set e2 global channel to 8 before attempting to receive.

e2syx2pat.py - Converts a pattern file in sysex format to pattern file in e2pat format.

e2seqrot.py - Rotates sequence of specified part by specified number of steps.  Takes e2pat as input.
