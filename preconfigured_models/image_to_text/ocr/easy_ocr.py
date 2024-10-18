def get_config():
    return {'repo': 'jinensetpal/autolabelling-models',
            'name': 'easy_ocr',
            'version': '2',
            'post_hook': post_hook,
            'pre_hook': pre_hook,
            'label_config': LABEL_CONFIG}

def pre_hook(paths):
    return paths

def post_hook(predictions):
    from uuid import uuid4
    result = []

    for prediction in list(predictions):
        width, height = prediction.orig_shape
        min_score = 1.
        if score < min_score: min_score = score
        result.append({
            'original_width': width,
            'original_height': height,
            'image_rotation': 0,
            'value': {
                "text": [prediction.result]
            },
            'id': str(uuid4())[:4],
            'from_name': 'image',
            'to_name': 'text',
            'type': 'textarea',
            'score': 1.,
            })
    return [{'result': result,
             'score': min_score,
             'model_version': '0.0.1'}]

LABEL_CONFIG = '<View>\n  <Image name="image" value="$ocr"/>\n\n  <Labels name="label" toName="image">\n    <Label value="Text" background="green"/>\n    <Label value="Handwriting" background="blue"/>\n  </Labels>\n\n  <Rectangle name="bbox" toName="image" strokeWidth="3"/>\n  <Polygon name="poly" toName="image" strokeWidth="3"/>\n\n  <TextArea name="transcription" toName="image"\n            editable="true"\n            perRegion="true"\n            required="true"\n            maxSubmissions="1"\n            rows="5"\n            placeholder="Recognized Text"\n            displayMode="region-list"\n            />\n</View>'
