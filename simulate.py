from dagshub.data_engine import datasources


def ls_polygon(predictions):
    result = []
    for prediction in list(predictions):
        width, height = prediction.orig_shape
        for idx, (mask, label_idx) in enumerate(zip(prediction.masks, prediction.boxes.cls.cpu().tolist())):
            result.append({'result': {'closed': True,
                                      'points': (prediction.masks.xyn[idx] * 100).astype(float).tolist(),
                                      'polygonlabels': [prediction.names[label_idx]]},
                           'model_version': '0.0.1'})
    return result

def brushlabels(predictions):
    from label_studio_sdk.converter import brush
    from uuid import uuid4
    results = []

    for prediction in list(predictions):
        result = []
        width, height = prediction.orig_shape
        for mask, label_idx in zip(prediction.masks, prediction.boxes.cls.cpu().tolist()):
            result.append({
                'id': str(uuid4())[:4],
                'from_name': 'tag',
                'to_name': 'image',
                'original_width': width,
                'original_height': height,
                'image_rotation': 0,
                'value': {
                    'format': 'rle',
                    'rle': brush.mask2rle(mask.data[0].numpy().astype(int) * 255),
                    'brushlabels': [prediction.names[label_idx]],
                    },
                'type': 'brushlabels',
                'readonly': False
                })
        results.append({'result': result, 'score': 1.})
    return results

def polygonlabels(predictions):
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


ds = datasources.get_datasource('jinensetpal/COCO_1K', 'COCO_1K')
ds.add_annotation_model('jinensetpal/COCO_1K', 'yolov8-seg', ls_polygon)

# q = ds.head(size=10)
# q.annotate_with_mlflow_model('jinensetpal/COCO_1K', 'yolov8-seg', polygonlabels, log_to_field='segmentation_annotation')
# ds.metadata_field('segmentation_annotation').set_annotation().apply()
