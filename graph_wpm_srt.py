# Script which reads an SRT (subtitle) file and
# charts the number of words per minute(s) as well
# as charting the contribution of each segment to
# the overal dialogue percentage.

# Input SRT might need to be converted to UTF-8 if
# provided in some other encoding. Rather than handle
# it here, I used iconv in the following way:
# `iconv -t utf8 input.srt > output.utf8.srt`


import pysrt
import matplotlib.pyplot as plt
import argparse


def convert_to_seconds(time):
    """
    00:34:23,234 ->
    00 hours, 34 mintes, 23,234 seconds
    """
    split = str(time).split(':')
    hr = int(split[0])
    mins = int(split[1])
    #sec = int(split[2].split(',')[0])
    sec = float(split[2].replace(',', '.'))

    return (hr*60*60) + (mins*60) + sec


def test(x, a, b):
    return a * np.sin(b * x)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input UTF-8 encoded SRT file UTF-8")
    parser.add_argument("-n", default=5, type=int, help="Number of minutes for each bucket. "\
                                    "Longer movies may need larger buckets (e.g. 10 minutes)")
    parser.add_argument("-m", default="Movie", help="Movie name (for plot title)")
    args = parser.parse_args()

    # Create subtitle segments from SRT
    srt_file = args.i
    subs = pysrt.open(srt_file)

    # Based on the last subtitle as a proxy for movie length (flawed),
    # determine how buckets of size N you need, where N is the number
    # of minutes per segment.
    last_sub = subs[-1]
    minute_chunk = args.n
    minute_buckets = round(convert_to_seconds(last_sub.end) / 60 / minute_chunk)

    wmp = [0] * minute_buckets          # track words per (n) minute(s)
    dialog_perc = [0] * minute_buckets  # track percentage of dialogue that has passed per (n) minutes


    # Iterate through subs to get full count of words
    # and total dialogue time. Exclude text which does
    # contain dialogue (typically marked up with <b>)

    total_word_count = 0
    total_speaking_time = 0

    for s in subs:
        if s.text.startswith('<b>'):
            continue
        words = s.text.split()
        total_word_count += len(words)
        start_seconds = (convert_to_seconds(s.start))
        end_seconds = (convert_to_seconds(s.end))
        total_speaking_time += (end_seconds - start_seconds)


    # Iterate through subs and aggregate words and percentage of
    # dialogue for each bucket of time

    for s in subs:
        if s.text.startswith('<b>'):
            continue
        words = s.text.split()  # simple whitespace tokenization
        start_seconds = (convert_to_seconds(s.start))
        end_seconds = (convert_to_seconds(s.end))
        duration = (end_seconds - start_seconds)

        # Determine which minute bucket a segment should be attributed to.
        # This will be done by rounding to the nearest N (minute bucket size)
        minute_buk = int(((round(end_seconds))/60/ minute_chunk))

        percent_dialog_spoken = duration/total_speaking_time*100  # calculate % of dialogue time-wise for this segment
        wmp[minute_buk-1] += len(words)  # words per segment added to the assigned "minute bucket"
        dialog_perc[minute_buk-1] += percent_dialog_spoken  # percentage of total speaking time per minute bucket


    # Create x,y axis data
    wmp_dataset = []
    dialog_perc_dataset = []
    for e,i in enumerate(wmp):
        wmp_dataset.append((e,i))

    running_total = 0
    for e,i in enumerate(dialog_perc):
        running_total += i
        #dialog_perc_dataset.append((e,i))  # if you want to see percentage of a segment, rather than cumulative percentage
        dialog_perc_dataset.append((e,running_total))


    x = [x[0] for x in wmp_dataset]
    y = [x[1] for x in wmp_dataset]
    x1 = [x[0] for x in dialog_perc_dataset]
    y1 = [x[1] for x in dialog_perc_dataset]


    # Create plot with 2 Y-Axes
    # First plot WPM
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Time Interval ({0} min)'.format(str(minute_chunk)))
    ax1.set_ylabel('Words Per (N) Minute(s)', color=color)
    ax1.plot(x, y, color=color)
    #ax1.plot(x, y, '-o', color=color)  # if you want individual points
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('% of Dialogue Completed', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, y1, color=color)
    #ax2.plot(x, y1, '-o', color=color)  # if you want individual points
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title(args.m)
    plt.show()


if __name__ == "__main__":
    main()
