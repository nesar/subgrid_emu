"""
Tests for the emulator module.
"""

import pytest
import numpy as np
from subgrid_emu import (
    load_emulator,
    list_available_statistics,
    AVAILABLE_STATS_5P,
    AVAILABLE_STATS_2P,
)


class TestEmulatorLoading:
    """Test emulator loading functionality."""

    def test_load_5p_emulator(self):
        """Test loading a 5-parameter emulator."""
        emu = load_emulator('GSMF')
        assert emu is not None
        assert emu.stat_name == 'GSMF'
        assert emu.n_params == 5

    def test_load_2p_emulator(self):
        """Test loading a 2-parameter emulator."""
        emu = load_emulator('CGD_2p')
        assert emu is not None
        assert emu.stat_name == 'CGD_2p'
        assert emu.n_params == 2

    def test_invalid_stat_name(self):
        """Test that invalid stat names raise appropriate errors."""
        with pytest.raises(ValueError):
            load_emulator('INVALID_STAT')

    def test_list_available_statistics(self):
        """Test listing available statistics."""
        stats = list_available_statistics()
        assert '5-parameter' in stats
        assert '2-parameter' in stats
        assert len(stats['5-parameter']) == len(AVAILABLE_STATS_5P)
        assert len(stats['2-parameter']) == len(AVAILABLE_STATS_2P)


class TestEmulatorPredictions:
    """Test emulator prediction functionality."""

    def test_5p_prediction_shape(self):
        """Test that 5-parameter predictions have correct shape."""
        emu = load_emulator('GSMF')
        params = [3.0, 0.5, 0.8, 0.65, 0.1]
        mean, quantiles = emu.predict(params)
        
        assert mean.shape[0] > 0
        assert quantiles.shape[0] == mean.shape[0]
        assert quantiles.shape[1] == 2  # [5%, 95%]

    def test_2p_prediction_shape(self):
        """Test that 2-parameter predictions have correct shape."""
        emu = load_emulator('fGas_2p')
        params = [0.65, 0.1]
        mean, quantiles = emu.predict(params)
        
        assert mean.shape[0] > 0
        assert quantiles.shape[0] == mean.shape[0]
        assert quantiles.shape[1] == 2

    def test_prediction_values_finite(self):
        """Test that predictions contain finite values."""
        emu = load_emulator('GSMF')
        params = [3.0, 0.5, 0.8, 0.65, 0.1]
        mean, quantiles = emu.predict(params)
        
        assert np.all(np.isfinite(mean))
        assert np.all(np.isfinite(quantiles))

    def test_quantiles_ordered(self):
        """Test that quantiles are properly ordered (5% < 95%)."""
        emu = load_emulator('GSMF')
        params = [3.0, 0.5, 0.8, 0.65, 0.1]
        mean, quantiles = emu.predict(params)
        
        assert np.all(quantiles[:, 0] <= quantiles[:, 1])

    def test_wrong_param_count_5p(self):
        """Test that wrong parameter count raises error for 5-param model."""
        emu = load_emulator('GSMF')
        params = [3.0, 0.5]  # Only 2 params instead of 5
        
        with pytest.raises((ValueError, IndexError)):
            emu.predict(params)

    def test_wrong_param_count_2p(self):
        """Test that wrong parameter count raises error for 2-param model."""
        emu = load_emulator('CGD_2p')
        params = [3.0, 0.5, 0.8, 0.65, 0.1]  # 5 params instead of 2
        
        with pytest.raises((ValueError, IndexError)):
            emu.predict(params)

    def test_multiple_predictions(self):
        """Test making multiple predictions."""
        emu = load_emulator('CSFR')
        params_list = [
            [3.0, 0.5, 0.8, 0.65, 0.1],
            [2.5, 0.7, 1.0, 0.5, 0.5],
            [3.5, 0.3, 0.9, 1.0, 0.2],
        ]
        
        for params in params_list:
            mean, quantiles = emu.predict(params)
            assert mean.shape[0] > 0
            assert np.all(np.isfinite(mean))


class TestAllEmulators:
    """Test all available emulators."""

    @pytest.mark.parametrize("stat_name", AVAILABLE_STATS_5P)
    def test_all_5p_emulators(self, stat_name):
        """Test that all 5-parameter emulators can be loaded and used."""
        emu = load_emulator(stat_name)
        params = [3.0, 0.5, 0.8, 0.65, 0.1]
        mean, quantiles = emu.predict(params)
        
        assert mean.shape[0] > 0
        assert np.all(np.isfinite(mean))
        assert np.all(np.isfinite(quantiles))

    @pytest.mark.parametrize("stat_name", AVAILABLE_STATS_2P)
    def test_all_2p_emulators(self, stat_name):
        """Test that all 2-parameter emulators can be loaded and used."""
        emu = load_emulator(stat_name)
        params = [0.65, 0.1]
        mean, quantiles = emu.predict(params)
        
        assert mean.shape[0] > 0
        assert np.all(np.isfinite(mean))
        assert np.all(np.isfinite(quantiles))
