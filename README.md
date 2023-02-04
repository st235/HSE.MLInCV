# Machine Learning in Computer Vision

## Image Segmentation: separate humans from background

A lightweight model to segment the prominent humans in the scene
in videos captured by a smartphone or web camera.
Runs in real-time (~120 FPS) on a laptop CPU via XNNPack TFLite backend.

Returns a two class segmentation label (human or background) per pixel.

| Original image                                            | Final classification                                                    |
|-----------------------------------------------------------|-------------------------------------------------------------------------|
| ![Original image](./resources/example_original_image.png) | ![Result classification](./resources/example_result_classification.png) |

### Build

__You need at least Python 3.9 to run the code.__

#### Virtual env

First of all, you need to activate virtual environment
in your folder using the command below. This step is optional,
however, can be very useful to segregate the project from your
global environment.

```bash
python3 -m venv .venv
```

Moreover, please, do pay attention, that the project uses [opencv contrib](https://pypi.org/project/opencv-contrib-python/).
So, if you're using global environment (instead of virtual) and have
opencv installed, please, do check if your version of opencv is the
right one.

When the environment is ready we can proceed with building the project.

#### Option 1: pip

The first option is to use `pip` to install the library. Use the command below to
download the code:

```bash
pip install git+https://github.com/st235/HSE.MLInCV.git
```

Pip should install all necessary dependencies and create an alias for the app.
The alias is `human-segmentation`.

To run the program just call the code below:

```bash
human-segmentation
```

The command will show default sample image similar to the next image.

![Sample image](./resources/sample_default.png)

To test the app against different image you can specify them as
the first argument. See the example below:

```bash
human-segmentation image1.png
```

#### Option 2: build from source

Alternatively, you can build the app from source.

Please, note that you need [build](https://pypi.org/project/build/) installed. To do so you need to run

```bash
pip install build
```

First step would be to build wheels from the source code. To do so you need to run __build__.

```bash
python3 -m build .
```

When the build is finished you are able to install the library from the produced wheel file.
A command can look like something below:

```bash
pip install dist/human_segmentation-0.0.1-py3-none-any.whl
```

It will start the same installation process as `pip` usually do. After the app is installed successfully
you may call it using `human-segmentation` command. For example,

```bash
human-segmentation
```

#### Option 3: build locally

And the last but not least is to run the app manually using [`demo.py`](./demo.py) script.

First of all, you need to install all necessary dependencies. Luckily,
all of them are located in [`requirements.txt`](./requirements.txt).
You need to run the following command to install all of them.

```bash
pip install -r requirements.txt
```

Now you're good to go! Hooray 🎉

To run the script you need to find a [demo file](./demo.py).
All source code is located under [src directory](./src).

You can use the next command to run the script to see the sample image:

```bash
python3 demo.py
```

and a slightly different command to test the app against different images:

```bash
python3 demo.py ./samples/house_01.png
```

As the result you will see something similar to the image below.

![Script results](./resources/script_output.png)

### Local development

To start local development in the repo, please, ensure that you have all code quality control tools installed.

To do so you need to run a few more commands __(additionally to the [local build commands](#option-3-build-locally))__
in the same order as below:

1. Install all dev dependencies, like, `linter`, `style formatter`, `pre-commit tools`, or `test runner`.

```
pip install -r dev-requirements.txt
```

2. Install pre-commit hooks. This step is not necessary, however, the same checks will be performed on the server side
when one creates Pull Request.

```
pre-commit install
```

#### Style formatter: black

- Code formatting tool
- Black configuration is located at [pyproject.toml](./pyproject.toml)
- To run black locally one may need to call `black .`

#### Linter: pylint

- Linter
- Pylint configuration is located at [pyproject.toml](./pyproject.toml)
- To run pylint locally one may need to call `pylint src`

#### Pre-commit

- Pre-commit hooks
- Configuration is located at [the special config](./.pre-commit-config.yaml)
- Command runs automatically on every commit, however, to manually test hooks one may want to call `pre-commit run --all-files`

#### Tests

You can run tests by executing the following command

```
pytest .
```

Moreover, this repository contains regression tests. Long story short: regression tests are assuming that the old
state of the system is correct, therefore at some point you need to generate them. To do so, just call `pytest` with
additional command `--overwrite-regression-result`.

See example below:

```
pytest . --overwrite-regression-result
```

### Misc

Code in this repo follows [Google's Python codestyle](https://google.github.io/styleguide/pyguide.html).
