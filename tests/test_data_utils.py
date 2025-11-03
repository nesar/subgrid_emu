"""
Tests for the data_utils module.
"""

import pytest
import numpy as np
from subgrid_emu import (
    get_x_grid,
    get_plot_info,
    get_valid_range,
    get_parameter_info,
    AVAILABLE_STATS_5P,
    AVAILABLE_STATS_2P,
)


class TestDataUtilities:
    """Test data utility functions."""

    @pytest.mark.parametrize("stat_name", AVAILABLE_STATS_5P + AVAILABLE_STATS_2P)
    def test_get_x_grid(self, stat_name):
        """Test getting x-axis grid for all statistics."""
        x_grid, x_label = get_x_grid(stat_name)
        
        assert isinstance(x_grid, np.ndarray)
        assert len(x_grid) > 0
        assert isinstance(x_label, str)
        assert len(x_label) > 0

    @pytest.mark.parametrize("stat_name", AVAILABLE_STATS_5P + AVAILABLE_STATS_2P)
    def test_get_plot_info(self, stat_name):
        """Test getting plot information for all statistics."""
        plot_info = get_plot_info(stat_name)
        
        assert 'title' in plot_info
        assert 'xlabel' in plot_info
        assert 'ylabel' in plot_info
        assert 'xscale' in plot_info
        assert 'yscale' in plot_info
        
        assert plot_info['xscale'] in ['linear', 'log']
        assert plot_info['yscale'] in ['linear', 'log']

    @pytest.mark.parametrize("stat_name", AVAILABLE_STATS_5P + AVAILABLE_STATS_2P)
    def test_get_valid_range(self, stat_name):
        """Test getting valid range for all statistics."""
        valid_range = get_valid_range(stat_name)
        
        assert isinstance(valid_range, tuple)
        assert len(valid_range) == 2
        assert valid_range[0] < valid_range[1]

    def test_get_parameter_info(self):
        """Test getting parameter information."""
        param_info = get_parameter_info()
        
        assert 'names' in param_info
        assert 'ranges' in param_info
        assert 'descriptions' in param_info
        assert 'scales' in param_info
        
        assert len(param_info['names']) == 5
        assert len(param_info['ranges']) == 5
        assert len(param_info['descriptions']) == 5
        assert len(param_info['scales']) == 3  # Only 3 parameters have scaling

    def test_invalid_stat_name_x_grid(self):
        """Test that invalid stat names raise errors in get_x_grid."""
        with pytest.raises(FileNotFoundError):
            get_x_grid('INVALID_STAT')

    def test_invalid_stat_name_plot_info(self):
        """Test that invalid stat names raise errors in get_plot_info."""
        with pytest.raises(ValueError):
            get_plot_info('INVALID_STAT')

    def test_invalid_stat_name_valid_range(self):
        """Test that invalid stat names raise errors in get_valid_range."""
        with pytest.raises(ValueError):
            get_valid_range('INVALID_STAT')
