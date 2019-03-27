# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
import os
import nbformat
import nbconvert

_nbdir = os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks')
_notebooks = [path
              for path in os.listdir(_nbdir)
              if path.endswith('.ipynb')]


@pytest.mark.parametrize("file", _notebooks)
@pytest.mark.notebook
def test_notebook(file):
    nb = nbformat.read(os.path.join(_nbdir, file), as_version=4)
    ep = nbconvert.preprocessors.ExecutePreprocessor(timeout=1500, allow_errors=True)
    ep.preprocess(nb, {'metadata': {'path': _nbdir}})
    errors = [nbconvert.preprocessors.CellExecutionError.from_cell_and_msg(cell, output)
              for cell in nb.cells if "outputs" in cell
              for output in cell["outputs"]
              if output.output_type == "error"]
    if errors:
        # TODO: should we apply html.unescape to the strings before concatenating them?
        err_str = "\n".join(str(err) for err in errors)
        raise AssertionError("Encountered {0} exception(s):\n{1}".format(len(errors), err_str))
