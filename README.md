## Plotting where the dialogue happens

This is a script which reads an SRT (subtitle) file and
charts the number of words per a certain number of minute(s) as well
as charting the contribution of each segment to the overal dialogue percentage.

Input SRT might need to be converted to UTF-8 if provided in some other encoding.
Rather than handle it in the script because I'm lazy, I used `iconv` in the following way:

`iconv -t utf8 input.srt > output.utf8.srt`

The script can be called as follows:

`python graph_wpm_srt.py -i samples/quiet.srt -m "A Quiet Place" -n 1`

```
usage: graph_wpm_srt.py [-h] [-i I] [-n N] [-m M]

optional arguments:
  -h, --help  show this help message and exit
  -i I        Input UTF-8 encoded SRT file UTF-8
  -n N        Number of minutes for each bucket. Longer movies may need larger
              buckets (e.g. 10 minutes)
  -m M        Movie name (for plot title)
```

Output will look like this:
![Sample Plot](/samples/quiet.png?raw=true)

Note: Movie length is based on the timestamp of the last subtitle entry which
is not ideal, but is a decent enough proxy.
