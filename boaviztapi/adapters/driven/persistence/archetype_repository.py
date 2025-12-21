"""Driven adapter: CSV/YAML-based archetype repository.

This module implements the IArchetypeRepository output port by reading
archetype data from CSV files in the data directory.
"""

import csv
import os
from typing import Dict, Any, Optional

from boaviztapi import data_dir, config
from boaviztapi.core.ports.output.archetype_repository import IArchetypeRepository
from boaviztapi.service.archetype import (
    get_archetype,
    row2json,
    get_device_archetype_lst
)


class ArchetypeRepository(IArchetypeRepository):
    """Driven Adapter: CSV-based archetype repository.
    
    Implements the IArchetypeRepository output port by loading archetype
    configurations from CSV files. This adapter bridges the application
    core with the file-based data storage.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize the archetype repository.
        
        Args:
            data_path: Path to data directory. If None, uses default data_dir
        """
        self._data_path = data_path or data_dir
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get_server_archetype(self, archetype_id: str) -> Optional[Dict[str, Any]]:
        """Get server archetype configuration by ID.
        
        Args:
            archetype_id: The archetype identifier (e.g., 'default')
            
        Returns:
            Dictionary containing archetype configuration or None if not found
        """
        if archetype_id == "default":
            archetype_id = config.get("default_server", "platform_compute_medium")
        
        cache_key = f"server:{archetype_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        csv_path = os.path.join(self._data_path, "archetypes/server.csv")
        archetype = get_archetype(archetype_id, csv_path)
        
        if archetype:
            self._cache[cache_key] = archetype
            return archetype
        return None
    
    def get_cloud_instance_archetype(
        self, 
        instance_type: str, 
        provider: str
    ) -> Optional[Dict[str, Any]]:
        """Get cloud instance archetype configuration.
        
        Args:
            instance_type: Type of cloud instance (e.g., 't2.micro')
            provider: Cloud provider (e.g., 'aws', 'azure', 'gcp')
            
        Returns:
            Dictionary containing archetype configuration or None if not found
        """
        cache_key = f"cloud:{provider}:{instance_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        csv_path = os.path.join(self._data_path, f"archetypes/cloud/{provider}.csv")
        
        if not os.path.exists(csv_path):
            return None
        
        archetype = get_archetype(instance_type, csv_path)
        
        if archetype:
            self._cache[cache_key] = archetype
            return archetype
        return None
    
    def get_component_archetype(
        self, 
        archetype_id: str, 
        component_type: str
    ) -> Optional[Dict[str, Any]]:
        """Get component archetype configuration.
        
        Args:
            archetype_id: The archetype identifier
            component_type: Type of component ('cpu', 'ram', 'disk', etc.)
            
        Returns:
            Dictionary containing archetype configuration or None if not found
        """
        cache_key = f"component:{component_type}:{archetype_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        csv_path = os.path.join(
            self._data_path, 
            f"archetypes/components/{component_type}.csv"
        )
        
        if not os.path.exists(csv_path):
            return None
        
        archetype = get_archetype(archetype_id, csv_path)
        
        if archetype:
            self._cache[cache_key] = archetype
            return archetype
        return None
    
    def get_iot_device_archetype(self, archetype_id: str) -> Optional[Dict[str, Any]]:
        """Get IoT device archetype configuration.
        
        Args:
            archetype_id: The archetype identifier
            
        Returns:
            Dictionary containing archetype configuration or None if not found
        """
        # Map "default" to configured default IoT device archetype
        if archetype_id == "default":
            archetype_id = config.get("default_iot_device", "iot-device-default")
        
        cache_key = f"iot:{archetype_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        csv_path = os.path.join(self._data_path, "archetypes/iot_device.csv")
        
        if not os.path.exists(csv_path):
            return None
        
        archetype = get_archetype(archetype_id, csv_path)
        
        if archetype:
            self._cache[cache_key] = archetype
            return archetype
        return None
    
    def get_user_terminal_archetype(self, archetype_id: str) -> Optional[Dict[str, Any]]:
        """Get user terminal (laptop, desktop, etc.) archetype configuration.
        
        Args:
            archetype_id: The archetype identifier
            
        Returns:
            Dictionary containing archetype configuration or None if not found
        """
        # Map "default" to configured default laptop archetype
        if archetype_id == "default":
            archetype_id = config.get("default_laptop", "laptop-pro")
        
        cache_key = f"terminal:{archetype_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        csv_path = os.path.join(self._data_path, "archetypes/user_terminal.csv")
        
        if not os.path.exists(csv_path):
            return None
        
        archetype = get_archetype(archetype_id, csv_path)
        
        if archetype:
            self._cache[cache_key] = archetype
            return archetype
        return None
    
    def list_device_archetypes(self) -> list:
        """List all available device archetypes.
        
        Returns:
            List of archetype configurations with metadata
        """
        archetypes = []
        
        archetype_files = {
            'server': 'archetypes/server.csv',
            'iot': 'archetypes/iot_device.csv',
            'terminal': 'archetypes/user_terminal.csv'
        }
        
        for device_type, rel_path in archetype_files.items():
            csv_path = os.path.join(self._data_path, rel_path)
            if os.path.exists(csv_path):
                arch_list = get_device_archetype_lst(csv_path)
                for arch_id in arch_list:
                    archetypes.append({
                        'device_type': device_type,
                        'archetype_id': arch_id
                    })
        
        return archetypes
    
    def list_available_archetypes(self, device_type: str) -> list:
        """List available archetypes for a device type.
        
        Args:
            device_type: Type of device ('server', 'cloud', 'iot', 'terminal')
            
        Returns:
            List of available archetype IDs
        """
        archetype_files = {
            'server': 'archetypes/server.csv',
            'iot': 'archetypes/iot_device.csv',
            'terminal': 'archetypes/user_terminal.csv'
        }
        
        if device_type not in archetype_files:
            return []
        
        csv_path = os.path.join(self._data_path, archetype_files[device_type])
        
        if not os.path.exists(csv_path):
            return []
        
        return get_device_archetype_lst(csv_path)
    
    def clear_cache(self) -> None:
        """Clear the archetype cache."""
        self._cache.clear()
