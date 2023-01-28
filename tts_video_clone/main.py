import argparse
from tts_video_clone.entry_points.synthesize_speech import synthesize_speech
def main():
    parser = argparse.ArgumentParser(prog='my_program')
    parser.add_argument('-t', '--text', type=str, help='file path to the text file')
    parser.add_argument('-i', '--input_vid', type=str, help='file path to the input_vid file')
    parser.add_argument('-o', '--output_vid', type=str, help='file path to the output_vid file')
    parser.add_argument('-d', '--duration', type=str, help='file path to the duration speechmarks file')
    args = parser.parse_args()
    # read the file as a string
    with open(args.text, 'r') as f:
        text = f.read()
    # pass the text to subcommand1
    synthesize_speech(text)


if __name__ == '__main__':
    main()
