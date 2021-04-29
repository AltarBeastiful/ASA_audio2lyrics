docker run -v C:\Users\RemiBENOIT\Documents\projects\mytest\data\\://a2l/dataset -it alta:latest

source /root/miniconda3/etc/profile.d/conda.sh
conda activate ALTA
./run_lyrics_alignment_long.sh "/a2l/dataset/wav/bar.mp3" "/a2l/dataset/lyrics/bar.txt" results
./run_lyrics_alignment_long.sh "dataset/wav/bar.mp3" "dataset/lyrics/bar.txt" results

apt-get install dos2unix
find . -type f -print0 | xargs -0 dos2unix