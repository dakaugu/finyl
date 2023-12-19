### Generating a new voice audio
To generate a new audio voice, run this command:<br>
```shell
tts --text "Text for TTS" \
    --model_name "<type>/<language>/<dataset>/<model_name>" \
    --out_path finyl/sounds/name.wav
```
The preferred convention for saving an audio is `finyl/sounds/audio_name.wav` <br>
Once completed, add your file to `sound.__init__.py`
```
EXAMPLE_SOUND_NAME = f"{BASE}/<sound_name>.wav"
```