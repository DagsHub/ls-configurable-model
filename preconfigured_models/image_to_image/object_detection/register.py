import mlflow
from ultralytics import YOLO
import dagshub

class CustomYOLO(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        # Attempt to load a custom model artifact if it exists
        artifact_path = context.artifacts.get("model", None)
        if artifact_path:
            # If there's a model artifact, load it (assuming it's compatible with EasyOCR)
            self.model = YOLO(context.artifacts['path'], task='detect')
        else:
            # Load the default model if no artifact is provided
            self.model = YOLO("yolov8n.pt", task='detect')

    def predict(self, context, img):
        preds = self.model(img)
        
        return preds

def register_model():
    # Switch to the destination MLflow tracking server
    dagshub.init(repo_owner='DagsHub', repo_name='ls-configurable-model', mlflow=True)
    
    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(
            artifact_path="model", # Assumes we have the artifact in a folder called "mlflow_model"
            code_paths=['register.py'],
            registered_model_name='object_detection',
            artifacts={'path': "model/model.pt"},
            python_model=CustomYOLO(),
            conda_env={
                'channels': ['defaults'],
                'dependencies': [
                    'python=3.12',
                    'pip',
                    {
                        'pip': [
                            '-r requirements.txt',
                        ]
                    }
                ]
            }
        )