"""Output port for accessing archetype data.

This interface defines the contract for retrieving archetype configurations
for devices and components. The application core uses this interface to 
fetch archetype data, and driven adapters (like CSV file readers) implement it.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class IArchetypeRepository(ABC):
    """Output Port: Interface for accessing archetype data.
    
    The application core uses this interface to retrieve archetype
    configurations for devices, components, and cloud instances.
    Driven adapters implement this interface to provide data from
    CSV files, databases, or other sources.
    """
    
    @abstractmethod
    def get_server_archetype(self, archetype_id: str) -> Optional[Dict[str, Any]]:
        """Get server archetype configuration by ID.
        
        Args:
            archetype_id: The archetype identifier (e.g., 'default')
            
        Returns:
            Dictionary containing archetype configuration or None if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def get_iot_device_archetype(self, archetype_id: str) -> Optional[Dict[str, Any]]:
        """Get IoT device archetype configuration.
        
        Args:
            archetype_id: The archetype identifier
            
        Returns:
            Dictionary containing archetype configuration or None if not found
        """
        pass
    
    @abstractmethod
    def get_user_terminal_archetype(self, archetype_id: str) -> Optional[Dict[str, Any]]:
        """Get user terminal archetype configuration.
        
        Args:
            archetype_id: The archetype identifier
            
        Returns:
            Dictionary containing archetype configuration or None if not found
        """
        pass
    
    @abstractmethod
    def list_device_archetypes(self) -> List[Dict[str, Any]]:
        """List all available device archetypes.
        
        Returns:
            List of archetype configurations with metadata
        """
        pass