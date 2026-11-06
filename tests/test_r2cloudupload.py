#!/usr/bin/env python

"""Tests for `r2cloudupload` package."""

import pytest
from src.r2cloudupload.nodes import R2CloudUpload

@pytest.fixture
def example_node():
    """Fixture to create an Example node instance."""
    return R2CloudUpload()

def test_example_node_initialization(example_node):
    """Test that the node can be instantiated."""
    assert isinstance(example_node, R2CloudUpload)

def test_return_types():
    """Test the node's metadata."""
    assert R2CloudUpload.RETURN_TYPES == ("str",)
    assert R2CloudUpload.FUNCTION == "test"
    assert R2CloudUpload.CATEGORY == "cloud"
