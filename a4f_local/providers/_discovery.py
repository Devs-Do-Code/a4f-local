import importlib
import pkgutil
import os
import logging
from typing import Dict, List, Callable, Any, Optional

logger = logging.getLogger(__name__)

# Registry to hold discovered engine functions: { 'provider_1': {'tts': create_speech_func}, ... }
PROVIDER_REGISTRY: Dict[str, Dict[str, Callable]] = {}
# Registry to hold discovered capabilities per provider: { 'provider_1': ['tts'], ... }
PROVIDER_CAPABILITIES: Dict[str, List[str]] = {}
# Optional: Store provider metadata like human-readable names
PROVIDER_METADATA: Dict[str, Dict[str, Any]] = {}

def find_providers():
    """
    Scans the 'providers' directory dynamically, imports provider modules,
    reads their capabilities, imports corresponding engine modules, and populates
    the PROVIDER_REGISTRY and PROVIDER_CAPABILITIES.
    """
    global PROVIDER_REGISTRY, PROVIDER_CAPABILITIES, PROVIDER_METADATA
    # Clear registries to allow for potential re-discovery if needed
    PROVIDER_REGISTRY.clear()
    PROVIDER_CAPABILITIES.clear()
    PROVIDER_METADATA.clear()

    providers_package_path = os.path.dirname(__file__) # Path to the 'providers' directory
    logger.info(f"Scanning for providers in: {providers_package_path}")

    # Use the package context for relative imports
    current_package = __package__ or 'a4f_local.providers'

    for _, provider_name, is_pkg in pkgutil.iter_modules([providers_package_path]):
        # Look for subdirectories that are packages and follow the naming convention
        if is_pkg and provider_name.startswith("provider_"):
            logger.debug(f"Found potential provider package: {provider_name}")
            try:
                # Import the provider's __init__.py to get capabilities and metadata
                provider_module_path = f".{provider_name}" # Relative import path
                provider_init = importlib.import_module(provider_module_path, package=current_package)

                if hasattr(provider_init, 'CAPABILITIES') and isinstance(provider_init.CAPABILITIES, list):
                    capabilities = provider_init.CAPABILITIES
                    PROVIDER_CAPABILITIES[provider_name] = capabilities
                    PROVIDER_REGISTRY[provider_name] = {} # Initialize registry for this provider
                    PROVIDER_METADATA[provider_name] = {
                        'name': getattr(provider_init, 'PROVIDER_NAME', provider_name) # Get optional name
                    }
                    logger.info(f"Discovered provider '{provider_name}' with capabilities: {capabilities}")

                    # Dynamically import the engine module for each declared capability
                    for capability in capabilities:
                        try:
                            capability_module_path = f".{provider_name}.{capability}"
                            capability_module = importlib.import_module(capability_module_path, package=current_package)

                            # --- Engine Function Discovery Convention ---
                            # Assume the capability module's __init__.py exports the main engine function,
                            # OR look for a conventionally named function (e.g., create_{capability}).
                            # Option 1: Check __all__ if defined in capability/__init__.py
                            engine_func = None
                            if hasattr(capability_module, '__all__') and capability_module.__all__:
                                engine_func_name = capability_module.__all__[0] # Assume first is the entry point
                                if hasattr(capability_module, engine_func_name):
                                    engine_func = getattr(capability_module, engine_func_name)
                            else:
                                # Option 2: Fallback to convention if __all__ is not helpful
                                conventional_func_name = f"create_{capability}" # e.g., create_tts, create_chat
                                if hasattr(capability_module, conventional_func_name):
                                    engine_func = getattr(capability_module, conventional_func_name)

                            if engine_func and callable(engine_func):
                                PROVIDER_REGISTRY[provider_name][capability] = engine_func
                                logger.debug(f"  Registered engine for '{capability}' capability.")
                            else:
                                logger.warning(f"Could not find or register callable engine function for {provider_name}.{capability}")

                        except ImportError as e_cap:
                            logger.warning(f"Could not import capability module '{capability}' for provider '{provider_name}': {e_cap}")
                        except Exception as e_eng:
                             logger.error(f"Error processing engine for {provider_name}.{capability}: {e_eng}")

                else:
                    logger.warning(f"Skipping '{provider_name}': Does not have a valid 'CAPABILITIES' list in its __init__.py.")

            except ImportError as e_prov:
                logger.warning(f"Could not import provider module '{provider_name}': {e_prov}")
            except Exception as e_gen:
                 logger.error(f"Error processing provider '{provider_name}': {e_gen}")

    logger.info(f"Provider discovery complete. Registry: {list(PROVIDER_REGISTRY.keys())}")


def get_provider_for_capability(capability: str) -> Optional[str]:
    """
    Finds the first discovered provider that supports a given capability.
    Note: This uses a simple first-match strategy. Could be enhanced later
    (e.g., based on configuration, model compatibility, or priority).
    """
    for provider_name, capabilities in PROVIDER_CAPABILITIES.items():
        if capability in capabilities:
            logger.debug(f"Found provider '{provider_name}' for capability '{capability}'")
            return provider_name
    logger.warning(f"No provider found supporting capability: {capability}")
    return None

def get_engine(provider_name: str, capability: str) -> Optional[Callable]:
    """Gets the registered engine function for a specific provider and capability."""
    provider_engines = PROVIDER_REGISTRY.get(provider_name)
    if provider_engines:
        engine_func = provider_engines.get(capability)
        if engine_func:
            return engine_func
        else:
            logger.error(f"Capability '{capability}' not found in registry for provider '{provider_name}'")
    else:
        logger.error(f"Provider '{provider_name}' not found in registry.")
    return None

# --- Auto-run discovery when this module is imported ---
# This ensures the registry is populated when the client or other parts of the package need it.
find_providers()
