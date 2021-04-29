import argparse
import collections
from datetime import timedelta
from os import path
import re


class LRCGenerator:
    def main(self, lyrics_path, alignement_path, save_dir):
        lyrics_format = lyrics_path.split('.')[-1]
        utt_id = lyrics_path.split('.'+lyrics_format)[0].split('/')[-1]
        text = []
        utt2spk = []

        t = []
        with open(lyrics_path, 'r', encoding="utf-8") as r:
            for line in r.readlines():
                if line.replace('\n', '') != '':
                    lyrics_line = re.sub(
                        "[^A-Za-z0-9'\-,\.\!\? ]+", '', line.replace('\n', ''))
                    t.append(lyrics_line)

            t_raw = ' '.join(t).replace('  ', ' ')
            text.append(t_raw.upper())

        print("end")

        timings = []
        with open(alignement_path, 'r') as alignement:
            for line in alignement.readlines():
                result = line.replace('\n', '').split(' ')
                timings.append(
                    (result[2], float(result[0])*1000, float(result[1])*1000))

        result_file_path = path.join(save_dir, utt_id + ".lrc")
        with open(result_file_path, 'w', encoding="utf-8") as lrc:
            previous_word_end = 0.0
            for line in t:
                words = line.split(' ')
                wrote_line_start = False
                timing = None
                for word in words:
                    if timings[0][0] != self.get_id(word):
                        break

                    timing = timings.pop(0)
                    if not wrote_line_start:
                        lrc.write(f"[{self.convert_timing(previous_word_end)}]")
                        wrote_line_start = True

                    lrc.write(f"<{self.convert_timing(timing[1])}> {word} ")
                    previous_word_end = timing[2]

                    print(f"{word}: {timing}")
                lrc.write("\n")

    def get_id(self, word):
        return re.sub('[^A-Za-z0-9]+', '', word).upper()

    def convert_timing(self, timing: float):
        return "{:0>8}".format(str(timedelta(milliseconds=timing)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("lyrics_path", type=str, help="Path to lyrics")
    parser.add_argument("alignement_path", type=str,
                        help="Path to alignement file")
    parser.add_argument("save_dir", type=str,
                        help="path to save the data files")

    args = parser.parse_args()

    lyrics_path = args.lyrics_path
    alignement_path = args.alignement_path
    save_dir = args.save_dir
    LRCGenerator().main(lyrics_path, alignement_path, save_dir)
