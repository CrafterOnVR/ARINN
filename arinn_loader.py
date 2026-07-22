
import os
import yaml  # type: ignore
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='[LOADER] %(message)s')
logger = logging.getLogger(__name__)

CONFIG_PATH = "config_optimized.yaml"

def load_config(path=CONFIG_PATH):
    """Loads the optimized YAML configuration."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_model_path(config):
    """Ensures the model GGUF exists locally, downloading if necessary."""
    try:
        from huggingface_hub import hf_hub_download  # type: ignore
    except ImportError:
        logger.error("huggingface_hub not installed.")
        return None

    model_cfg = config["model"]
    repo_id = model_cfg["repo_id"]
    filename = model_cfg["filename"]
    local_dir = model_cfg.get("local_dir", "brain/models")
    
    # Create directory if missing
    os.makedirs(local_dir, exist_ok=True)
    
    target_path = os.path.join(local_dir, filename)
    
    if os.path.exists(target_path):
        logger.info(f"Model found locally: {target_path}")
        return target_path
        
    logger.info(f"Model not found. Downloading {filename} from {repo_id}...")
    try:
        downloaded_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        logger.info(f"Download complete: {downloaded_path}")
        return downloaded_path
    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise

def initialize_brain(config_path=CONFIG_PATH):
    """Initializes and returns the Llama instance based on config."""
    logger.info("Initializing Silicon Cortex (High-Performance Mode)...")
    
    try:
        # Import here to avoid crash if missing
        from llama_cpp import Llama  # type: ignore
    except ImportError:
        logger.critical("FATAL: `llama-cpp-python` is not installed.")
        logger.critical("Please install Visual Studio C++ Build Tools and run: pip install llama-cpp-python")
        return None, None

    try:
        config = load_config(config_path)
        model_path = get_model_path(config)
        if not model_path:
             return None, None

        inf_cfg = config["inference"]
        cache_cfg = config["cache"]
        
        logger.info(f"Loading Llama C++ with Context: {inf_cfg['n_ctx']}, GPU Layers: {inf_cfg['n_gpu_layers']}")
        
        llm = Llama(
            model_path=model_path,
            n_ctx=inf_cfg["n_ctx"],
            n_gpu_layers=inf_cfg["n_gpu_layers"],
            n_batch=inf_cfg["n_batch"],
            n_threads=inf_cfg["n_threads"],
            n_threads_batch=inf_cfg["n_threads_batch"],
            type_k=cache_cfg["type_k"] if hasattr(Llama, 'type_k') else None,
            type_v=cache_cfg["type_v"] if hasattr(Llama, 'type_v') else None,
            verbose=True
        )
        
        logger.info("Brain successfully loaded.")
        return llm, config
        
    except Exception as e:
        logger.critical(f"FATAL: Failed to initialize brain. Error: {e}")
        return None, None

if __name__ == "__main__":
    # Test the loader independently
    try:
        brain, cfg = initialize_brain()
        print("Success! System Prompt sample:")
        print(cfg["system_prompt"])  # type: ignore
    except Exception as e:
        print(f" Loader Test Failed: {e}")

# Genesis Compatibility Alias
load_arinn = initialize_brain
