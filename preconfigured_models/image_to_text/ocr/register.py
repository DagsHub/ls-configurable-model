import mlflow
import dagshub
import easyocr
import cv2

# Define a custom MLflow PythonModel for EasyOCR
class EasyOCRModel(mlflow.pyfunc.PythonModel):

    def load_context(self, context):
        # Attempt to load a custom model artifact if it exists
        artifact_path = context.artifacts.get("model", None)
        if artifact_path:
            # If there's a model artifact, load it (assuming it's compatible with EasyOCR)
            self.reader = easyocr.Reader(['en'], model_storage_directory=artifact_path)
        else:
            # Load the default model if no artifact is provided
            self.reader = easyocr.Reader(['en'])

    def predict(self, context, model_input):
        # Perform OCR using the EasyOCR model on the input image(s)
        # Assuming model_input is a list of image file paths
        results = []
        for image_path in model_input:
            image = cv2.imread(image_path)
            image_height, image_width = image.shape[:2]
            
            ocr_results = self.reader.readtext(image_path)

            formatted_results = []
            for result in ocr_results:
                bbox, text, score = result
                (top_left, top_right, bottom_right, bottom_left) = bbox

                # Calculate bounding box properties
                x_min = min(top_left[0], bottom_left[0])
                y_min = min(top_left[1], top_right[1])
                x_max = max(top_right[0], bottom_right[0])
                y_max = max(bottom_left[1], bottom_right[1])

                width = x_max - x_min
                height = y_max - y_min

                # Calculate properties in percentage relative to image dimensions
                x_percent = (x_min / image_width) * 100
                y_percent = (y_min / image_height) * 100
                width_percent = (width / image_width) * 100
                height_percent = (height / image_height) * 100

                formatted_results.append({
                    "x": x_percent,
                    "y": y_percent,
                    "width": width_percent,
                    "height": height_percent,
                    "text": [text],
                    "score": score,
                })

            results.append({
                "orig_shape": (image_width, image_height),
                "result": formatted_results,
            })
        return results

def register_model():
    # Switch to the destination MLflow tracking server
    dagshub.init(repo_owner='DagsHub', repo_name='ls-configurable-model', mlflow=True)
    
    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(
            code_paths=['register.py'],
            artifact_path="model", # Assumes we have the artifact in a folder called "mlflow_model"
            python_model=EasyOCRModel(),
        )
        model_uri = f"runs:/{run.info.run_id}/model"
        # Register the model to the destination registry
        model_name = "easy_ocr"  # Optionally, you can register it under a new name
        result = mlflow.register_model(model_uri=model_uri, name=model_name)
        
        print(f"Model registered to destination MLflow registry with name: {model_name}")