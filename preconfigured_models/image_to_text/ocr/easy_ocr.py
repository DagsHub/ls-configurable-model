def get_config():
    return {'repo': 'DagsHub/ls-configurable-model',
            'name': 'easy_ocr',
            'version': '1',
            'post_hook': post_hook,
            'pre_hook': pre_hook,
            'label_config': LABEL_CONFIG}

def pre_hook(paths):
    return paths

def post_hook(predictions):
    from uuid import uuid4
    result = []

    for prediction in list(predictions):      
        width, height = prediction["orig_shape"]
        min_score = 1.
        for res in prediction["result"]:
            uuid = uuid4().hex[:10]
            if res["score"] < min_score: min_score = res["score"]
            result.append({
                'original_width': width,
                'original_height': height,
                'image_rotation': 0,
                'value': {
                    "x": res["x"],
                    "y": res["y"],
                    "width": res["width"],
                    "height": res["height"],
                    "text": res["text"],
                    "rotation": 0,
                },
                'id': uuid,
                'from_name': 'transcription',
                'to_name': 'image',
                'type': 'textarea',
                'score': res["score"],
                })
            result.append({
                'original_width': width,
                'original_height': height,
                'image_rotation': 0,
                'value': {
                    "x": res["x"],
                    "y": res["y"],
                    "width": res["width"],
                    "height": res["height"],
                    "labels": ["Text"],
                    "rotation": 0,
                },
                'id': uuid,
                'from_name': 'label',
                'to_name': 'image',
                'type': 'labels',
                })
    return [{'result': result,
             'score': min_score,
             'model_version': '0.0.1'}]

LABEL_CONFIG = '<View>\n  <Image name="image" value="$image"/>\n\n  <Labels name="label" toName="image">\n    <Label value="Text" background="green"/>\n  </Labels>\n\n  <Rectangle name="bbox" toName="image" strokeWidth="3"/>\n\n  <TextArea name="transcription" toName="image"\n            editable="true"\n            perRegion="true"\n            required="true"\n            maxSubmissions="1"\n            rows="5"\n            placeholder="Recognized Text"\n            displayMode="region-list"\n            />\n</View>'
