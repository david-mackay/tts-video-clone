from setuptools import setup, find_packages

setup(
    name='my_program',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tts_clone = tts_video_clone.main:main',
            'synthesize_speech = tts_video_clone.entry_points:synthesize_speech',
            'overlay_strings = tts_video_clone.entry_points:overlay_strings'
        ]
    }
)