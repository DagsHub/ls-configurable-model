from uuid import uuid4


def post_hook(predictions):
    result = []
    for prediction in list(predictions):
        width, height = prediction.orig_shape
        min_score = 1.
        for idx, (mask, label_idx, score) in enumerate(zip(prediction.masks, prediction.boxes.cls.cpu().tolist(), prediction.boxes.conf.tolist())):
            if score < min_score: min_score = score
            result.append({'id': str(uuid4())[:4],
                           'from_name': 'label',
                           'to_name': 'image',
                           'original_width': width,
                           'original_height': height,
                           'image_rotation': 0,
                           'value': {
                               'closed': True,
                               'points': (prediction.masks.xyn[idx] * 100).astype(float).tolist(),
                               'polygonlabels': [prediction.names[label_idx]],
                               'score': score},
                           'type': 'polygonlabels',
                           'readonly': False})
    return [{'result': result,
             'score': min_score,
             'model_version': '0.0.1'}]


def query_result_post_hook(predictions):
    from uuid import uuid4
    results = []

    for prediction in list(predictions):
        result = []
        width, height = prediction.orig_shape
        for idx, (mask, label_idx) in enumerate(zip(prediction.masks, prediction.boxes.cls.cpu().tolist())):
            result.append({
                'id': str(uuid4())[:4],
                'from_name': 'tag',
                'to_name': 'image',
                'original_width': width,
                'original_height': height,
                'image_rotation': 0,
                'value': {
                    'closed': True,
                    'points': (prediction.masks.xyn[idx] * 100).astype(float).tolist(),
                    'polygonlabels': [prediction.names[label_idx]],
                },
                'type': 'polygonlabels',
                'readonly': False,
                'score': 1.
                })
        results.append({'result': result, 'score': 1})
    return results
