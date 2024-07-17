# Configurable Backend

This project allows you to create a custom LabelStudio backend from any MLFlow model hosted on DagsHub.

## Introduction

Setting up a LabelStudio Backend is a long and tedious process. Large parts can be automated if your model is connected via MLflow, and this project helps set such a system up. 

Users have two points of injection: a `post_hook` and a `pre_hook`. The `pre_hook` takes as input a local filepath to the downloaded datapoint for annotation, which is then forwarded to the MLflow model for prediction, which finally is forwarded to the `post_hook` for conversion to the LS format.

The `pre_hook` is optional, and defaults to the identity function `lambda x: x`.

## Steps for Setup

1. Pull git submodules `git submodule update --init`.
2. From the project root, build a docker container with the label 'configurable-ls-backend': `docker build . -t configurable-ls-backend`
3. From here, you can either run a docker container, or a container orchestrator (multiple containers with multiple backends).
  a. Docker container: `docker run configurable-ls-backend -p <port-of-choice>:9090`
  a. Orchestrator: `flask --app orchestrator run`

The backend is now ready. now we move to the client.

4. pip install git+https://github.com/DagsHub/client@ls-remote+mlflow

Once this is working, you're ready to use any MLflow model as a LS backend. The last thing left to supply is hooks, one that processes filepaths into the desired input, and one that takes the predictions from an MLflow model and converts them into the LabelStudio format. Refer to the following section for details on building a post hook.

5. Since datapoints (which are sent for annotation) are each associated with datasources, you must first initialize a datasource before you can add an annotation model to a desired annotation project.
```python
In [1]: from dagshub.data_engine import datasources
In [2]: from hooks.polygon_segmentation import post_hook
In [3]: ds = datasources.get_datasource('username/repo', 'datasource_name')
```

6. To add an annotation model, specify the repo it's registered under, the model name, as well as the post hook. This will supply an endpoint URL you can forward and add to LabelStudio. Optionally, you can also provide an ngrok token and a project name, and the client will forward and add the endpoint for you as well.
```python
In [4]: ds.add_annotation_model('username/repo', 'model_name', post_hook)
```
For more information about additional options you can supply, refer to `help(ds.add_annotation_model)`.

## Building Post Hooks

The key task that remains is that of setting up a `post_hook`. This can be tricky, because failure is not always explicit. Refer to the following sections on tips for debugging, to ease that process.

The key idea is that the model expects a list of predictions for each annotation task (different image, different prediction),

A prediction consists of a dictionary containing `result`, `score`, and `model_version` keys.

The `result` key contains a list of results (e.g. multiple instances of an object on a single image), which further contain an `id` that must be generated randomly, information about the target, the type of the prediction, as well as the value of the prediction itself. While the values passed varies between tasks, the overall key structure is retained, and following it is crucial to having everything render correctly.

An example of a predictions JSON is as follows (points trimmed for convenience):
```json
  "predictions": [
    {
      "id": 30,
      "model_version": "0.0.1",
      "created_ago": "23 hours, 41 minutes",
      "result": [
        {
          "id": "f346",
          "type": "polygonlabels",
          "value": {
            "score": 0.8430982828140259,
            "closed": true,
            "points": [ ... ],
            "polygonlabels": [
              "giraffe"
            ]
          },
          "to_name": "image",
          "readonly": false,
          "from_name": "label",
          "image_rotation": 0,
          "original_width": 426,
          "original_height": 640
        }
      ],
      "score": 0.8430982828140259,
      "cluster": null,
      "neighbors": null,
      "mislabeling": 0,
      "created_at": "2024-07-16T12:56:49.517014Z",
      "updated_at": "2024-07-16T12:56:49.517042Z",
      "task": 7,
      "project": 3
    }
  ]
```

# Tips for Debugging & Hassle-Free Development
1. Use `label-studio-ml start .` locally to not have to rebuild your docker container after every build.
2. A local instance of Label Studio is helpful for understanding cases wherein the prediction did not render correctly. My recommendation is to inject `IPython.embed()` strategically within `predict_tasks` from `label_studio.ml.models` to identify if there's a discrepancy between what you expect and what you see. For this to works within `model.py`, change `tasks` from L30 to a list containing a path that you know contains valid targets.
    a. If you opt for this, use a separate virtual environment for label-studio.
3. Remember that for cloudpickle to work, you need to have the docker container set up with the same version as that used to send the command to the container. Therefore, you may have to rebuild the container to match that. You can test if this is working correctly by running `print(inspect.getsourcecode(self.post_hook))` in `model.py`.
4. Include all your dependencies from hooks to the registered mlflow model.
5. Ensure that the MLFlow model that you are running works dependency-free. Incorrectly registered models may be missing code files, not have a signature or may be missing dependencies.
6. Once you initialize a docker container, running configure multiple times will reset it completely, and the docker container need not be restarted.
7. For unknown json formats, you can use the task source `</>` button in LabelStudio's task view to reveal the source JSON, which you can use as a reference to build a functional prediction.
