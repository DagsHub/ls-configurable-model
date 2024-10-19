def get_config():
    return {'repo': 'DagsHub/ls-configurable-model',
            'name': 'polygon_segmentation',
            'version': '6',
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

LABEL_CONFIG = '<View>\n\n  <Header value="Select label and click the image to start"/>\n  <Image name="image" value="$image" zoom="true"/>\n\n  <PolygonLabels name="label" toName="image" strokeWidth="3" pointSize="small" opacity="0.9">\n    \n    \n  <Label value="person" background="#FFA39E"/><Label value="bicycle" background="#D4380D"/><Label value="car" background="#FFC069"/><Label value="motorcycle" background="#AD8B00"/><Label value="airplane" background="#D3F261"/><Label value="bus" background="#389E0D"/><Label value="train" background="#5CDBD3"/><Label value="truck" background="#096DD9"/><Label value="boat" background="#ADC6FF"/><Label value="traffic light" background="#9254DE"/><Label value="fire hydrant" background="#F759AB"/><Label value="stop sign" background="#FFA39E"/><Label value="parking meter" background="#D4380D"/><Label value="bench" background="#FFC069"/><Label value="bird" background="#AD8B00"/><Label value="cat" background="#D3F261"/><Label value="dog" background="#389E0D"/><Label value="horse" background="#5CDBD3"/><Label value="sheep" background="#096DD9"/><Label value="cow" background="#ADC6FF"/><Label value="elephant" background="#9254DE"/><Label value="bear" background="#F759AB"/><Label value="zebra" background="#FFA39E"/><Label value="giraffe" background="#D4380D"/><Label value="backpack" background="#FFC069"/><Label value="umbrella" background="#AD8B00"/><Label value="handbag" background="#D3F261"/><Label value="tie" background="#389E0D"/><Label value="suitcase" background="#5CDBD3"/><Label value="frisbee" background="#096DD9"/><Label value="skis" background="#ADC6FF"/><Label value="snowboard" background="#9254DE"/><Label value="sports ball" background="#F759AB"/><Label value="kite" background="#FFA39E"/><Label value="baseball bat" background="#D4380D"/><Label value="baseball glove" background="#FFC069"/><Label value="skateboard" background="#AD8B00"/><Label value="surfboard" background="#D3F261"/><Label value="tennis racket" background="#389E0D"/><Label value="bottle" background="#5CDBD3"/><Label value="wine glass" background="#096DD9"/><Label value="cup" background="#ADC6FF"/><Label value="fork" background="#9254DE"/><Label value="knife" background="#F759AB"/><Label value="spoon" background="#FFA39E"/><Label value="bowl" background="#D4380D"/><Label value="banana" background="#FFC069"/><Label value="apple" background="#AD8B00"/><Label value="sandwich" background="#D3F261"/><Label value="orange" background="#389E0D"/><Label value="broccoli" background="#5CDBD3"/><Label value="carrot" background="#096DD9"/><Label value="hot dog" background="#ADC6FF"/><Label value="pizza" background="#9254DE"/><Label value="donut" background="#F759AB"/><Label value="cake" background="#FFA39E"/><Label value="chair" background="#D4380D"/><Label value="couch" background="#FFC069"/><Label value="potted plant" background="#AD8B00"/><Label value="bed" background="#D3F261"/><Label value="dining table" background="#389E0D"/><Label value="toilet" background="#5CDBD3"/><Label value="tv" background="#096DD9"/><Label value="laptop" background="#ADC6FF"/><Label value="mouse" background="#9254DE"/><Label value="remote" background="#F759AB"/><Label value="keyboard" background="#FFA39E"/><Label value="cell phone" background="#D4380D"/><Label value="microwave" background="#FFC069"/><Label value="oven" background="#AD8B00"/><Label value="toaster" background="#D3F261"/><Label value="sink" background="#389E0D"/><Label value="refrigerator" background="#5CDBD3"/><Label value="book" background="#096DD9"/><Label value="clock" background="#ADC6FF"/><Label value="vase" background="#9254DE"/><Label value="scissors" background="#F759AB"/><Label value="teddy bear" background="#FFA39E"/><Label value="hair drier" background="#D4380D"/><Label value="toothbrush" background="#FFC069"/></PolygonLabels>\n\n</View>'
