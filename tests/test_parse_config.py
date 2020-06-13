import pytest
import os
from skraped.config.parser import base_path, DEFAULT_SETTINGS_PATH, parse_yaml_args, parse_config

def test_parse_config(tmpdir):
    file_not_found = os.path.join(tmpdir, "settings.yaml")
    with pytest.raises(FileNotFoundError):
        parse_yaml_args(file_not_found)
    parsed_config = parse_config([])
    assert "Glassdoor" in parsed_config.get("sources")
