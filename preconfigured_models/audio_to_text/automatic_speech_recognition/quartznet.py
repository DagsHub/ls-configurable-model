#!/usr/bin/env python3

def pre_hook(paths):
    return paths


def post_hook(predictions):
    from uuid import uuid4

    result = []
    for prediction in predictions:
        result.append({'id': str(uuid4())[:4],
                       'from_name': 'transcription',
                       'to_name': 'audio',
                       'value': {
                           'text': [prediction]},
                       'type': 'textarea'})
    return [{'result': result,
             'score': .1,
             'model_version': '0.0.1'}]

LABEL_CONFIG = '<View>\n  <Audio name="audio" value="$audio" zoom="true" hotkey="ctrl+enter" />\n  <Header value="Provide Transcription" />\n  <TextArea name="transcription" toName="audio"\n            rows="4" editable="true" maxSubmissions="1" />\n</View>'
