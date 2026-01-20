# -*- coding: utf-8 -*-
"""
union_config.py v1.0.0
EriAmo Union - Configuration

Centralized configuration for Union system.
"""

import os


class UnionConfig:
    """
    Centralized configuration for EriAmo Union.
    
    Modify these values to customize Union behavior.
    """
    
    # =========================================================================
    # VERSION & META
    # =========================================================================
    
    VERSION = "1.0.0-Phase1"
    PHASE = "Phase 1 - Basic Routing"
    
    # =========================================================================
    # FILE PATHS
    # =========================================================================
    
    # Language soul files
    LANGUAGE_SOUL_FILE = "eriamo.soul"
    LANGUAGE_LEXICON_FILE = "lexicon.soul"
    
    # Music soul files
    MUSIC_HISTORY_FILE = "data/soul_history.csv"
    MUSIC_DUMPS_DIR = "data/dumps"
    
    # Union soul file (Phase 3)
    UNION_SOUL_FILE = "data/union_soul/unified.soul"
    
    # =========================================================================
    # BEHAVIOR SETTINGS
    # =========================================================================
    
    # General
    VERBOSE = True  # Print detailed logs
    LANGUAGE_ONLY = False  # Skip music system (for testing)
    
    # Phase 2: Axis Mapping (not yet implemented)
    AUTO_SYNC = False  # Automatically sync emotional states
    SYNC_INTERVAL = 1.0  # Seconds between syncs (if auto)
    
    # Phase 3: Memory (not yet implemented)
    UNIFIED_MEMORY = False  # Use unified D_Map
    
    # Phase 4: Agency (not yet implemented)
    AUTONOMOUS_CREATION = False  # Enable autonomous creative actions
    
    # =========================================================================
    # THRESHOLDS & PARAMETERS
    # =========================================================================
    
    # Axis mapping (Phase 2)
    EMOTION_SYNC_STRENGTH = 0.1  # How strongly emotions affect ontological axes
    ONTOLOGICAL_SYNC_STRENGTH = 0.1  # How strongly ontological affects emotions
    
    # Memory (Phase 3)
    MEMORY_RECALL_THRESHOLD = 0.3  # Minimum similarity for recall
    MAX_RECALL_RESULTS = 5  # Maximum number of memories to recall
    
    # Creative agency (Phase 4)
    CREATIVE_THRESHOLD_HIGH = 0.7  # High creativity trigger
    CREATIVE_THRESHOLD_MEDIUM = 0.5  # Medium creativity trigger
    
    # =========================================================================
    # SYSTEM CHECKS
    # =========================================================================
    
    @classmethod
    def validate_environment(cls):
        """
        Validate that environment is properly set up.
        
        Returns:
            tuple: (success: bool, messages: list)
        """
        messages = []
        success = True
        
        # Check Language soul file
        if not os.path.exists(cls.LANGUAGE_SOUL_FILE):
            messages.append(f"⚠ Warning: {cls.LANGUAGE_SOUL_FILE} not found")
            messages.append("  Language system will create new soul")
        
        # Check data directory
        if not os.path.exists("data"):
            messages.append("ℹ Info: Creating data/ directory")
            try:
                os.makedirs("data", exist_ok=True)
            except Exception as e:
                messages.append(f"❌ Error creating data/: {e}")
                success = False
        
        # Check union_soul directory (Phase 3)
        union_soul_dir = os.path.dirname(cls.UNION_SOUL_FILE)
        if not os.path.exists(union_soul_dir):
            messages.append(f"ℹ Info: Creating {union_soul_dir}/ directory")
            try:
                os.makedirs(union_soul_dir, exist_ok=True)
            except Exception as e:
                messages.append(f"⚠ Warning: Could not create {union_soul_dir}/: {e}")
        
        return success, messages
    
    @classmethod
    def print_config(cls):
        """Print current configuration."""
        print("\n" + "="*70)
        print("  ⚙️  EriAmo Union Configuration")
        print("="*70)
        print(f"Version: {cls.VERSION}")
        print(f"Phase: {cls.PHASE}")
        
        print("\n📂 Paths:")
        print(f"  Language soul: {cls.LANGUAGE_SOUL_FILE}")
        print(f"  Music history: {cls.MUSIC_HISTORY_FILE}")
        print(f"  Union soul: {cls.UNION_SOUL_FILE}")
        
        print("\n⚙️  Behavior:")
        print(f"  Verbose: {cls.VERBOSE}")
        print(f"  Language only: {cls.LANGUAGE_ONLY}")
        print(f"  Auto-sync: {cls.AUTO_SYNC} (Phase 2)")
        print(f"  Unified memory: {cls.UNIFIED_MEMORY} (Phase 3)")
        print(f"  Autonomous creation: {cls.AUTONOMOUS_CREATION} (Phase 4)")
        
        print("\n🎯 Thresholds:")
        print(f"  Emotion sync: {cls.EMOTION_SYNC_STRENGTH}")
        print(f"  Memory recall: {cls.MEMORY_RECALL_THRESHOLD}")
        print(f"  Creative (high): {cls.CREATIVE_THRESHOLD_HIGH}")
        
        print("="*70 + "\n")
    
    @classmethod
    def check_dependencies(cls):
        """
        Check if required dependencies are installed.
        
        Returns:
            tuple: (success: bool, missing: list)
        """
        required = [
            'numpy',
            'pandas',  # For music system
            'matplotlib',  # For music system
        ]
        
        optional = [
            'music21',  # For advanced music analysis
            'plotly',  # For visualization
            'pytest',  # For testing
        ]
        
        missing_required = []
        missing_optional = []
        
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                missing_required.append(pkg)
        
        for pkg in optional:
            try:
                __import__(pkg)
            except ImportError:
                missing_optional.append(pkg)
        
        return len(missing_required) == 0, missing_required, missing_optional


# =============================================================================
# QUICK CHECK
# =============================================================================

def quick_check():
    """Run quick environment check."""
    print("\n🔍 Running environment check...\n")
    
    # Print config
    UnionConfig.print_config()
    
    # Validate environment
    print("📋 Validating environment...")
    success, messages = UnionConfig.validate_environment()
    
    for msg in messages:
        print(f"  {msg}")
    
    if success:
        print("  ✅ Environment OK")
    else:
        print("  ❌ Environment has issues")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    success, missing_req, missing_opt = UnionConfig.check_dependencies()
    
    if missing_req:
        print(f"  ❌ Missing required: {', '.join(missing_req)}")
        print(f"     Install with: pip install {' '.join(missing_req)}")
    else:
        print("  ✅ All required dependencies installed")
    
    if missing_opt:
        print(f"  ℹ️  Missing optional: {', '.join(missing_opt)}")
        print(f"     Install with: pip install {' '.join(missing_opt)}")
    else:
        print("  ✅ All optional dependencies installed")
    
    print("\n" + "="*70 + "\n")
    
    return success and len(missing_req) == 0


if __name__ == "__main__":
    quick_check()
