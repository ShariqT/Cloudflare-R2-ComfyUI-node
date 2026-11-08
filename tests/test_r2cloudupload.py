#!/usr/bin/env python

"""Tests for `r2cloudupload` package."""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.r2cloudupload.nodes import R2CloudUpload


@pytest.fixture
def r2_upload_node():
    """Fixture to create an R2CloudUpload node instance."""
    return R2CloudUpload()


def test_node_initialization(r2_upload_node):
    """Test that the node can be instantiated."""
    assert isinstance(r2_upload_node, R2CloudUpload)


def test_return_types():
    """Test the node's metadata."""
    assert R2CloudUpload.RETURN_TYPES == ("STRING",)
    assert R2CloudUpload.FUNCTION == "upload"
    assert R2CloudUpload.CATEGORY == "image"
    assert R2CloudUpload.OUTPUT_NODE == True


def test_input_types_structure():
    """Test that INPUT_TYPES has the correct structure."""
    input_types = R2CloudUpload.INPUT_TYPES()
    
    # Check required fields
    required_fields = ['image', 'bucket_name', 'account_id', 'access_key_id', 
                       'secret_access_key', 'public_url_base']
    for field in required_fields:
        assert field in input_types['required'], f"Missing required field: {field}"
    
    # Check optional fields
    assert 'file_name' in input_types['optional']


def test_display_name_mapping():
    """Test that display name mapping is correct."""
    from src.r2cloudupload.nodes import NODE_DISPLAY_NAME_MAPPINGS
    assert NODE_DISPLAY_NAME_MAPPINGS['R2CloudUpload'] == 'R2 Cloud Upload'


def test_upload_missing_credentials(r2_upload_node):
    """Test that upload raises error when credentials are missing."""
    test_image = np.array([[[1.0, 0.0, 0.0]]])
    
    with pytest.raises(ValueError, match="All R2 credentials"):
        r2_upload_node.upload(
            image=[test_image],
            bucket_name='',
            account_id='test-account',
            access_key_id='test-key',
            secret_access_key='test-secret',
            public_url_base='https://test.r2.dev',
            file_name='test.png'
        )


def test_class_mappings():
    """Test that NODE_CLASS_MAPPINGS is correctly defined."""
    from src.r2cloudupload.nodes import NODE_CLASS_MAPPINGS
    assert 'R2CloudUpload' in NODE_CLASS_MAPPINGS
    assert NODE_CLASS_MAPPINGS['R2CloudUpload'] == R2CloudUpload


def test_description():
    """Test that the node has a description."""
    assert R2CloudUpload.DESCRIPTION is not None
    assert len(R2CloudUpload.DESCRIPTION) > 0
