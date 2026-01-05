# -*- coding: utf-8 -*-
"""
soul_migrator.py v1.0.0-Phase3
EriAmo Union - Soul Migration Tool

Migrates existing Language and Music souls into unified memory format.

Author: Claude & Maciej
Date: December 19, 2025
"""

import json
import numpy as np
from typing import Dict, Any, Optional
import os

from unified_memory import UnifiedMemory


class SoulMigrator:
    """
    Migrate existing Language and Music souls into unified memory.
    
    Handles:
    - Language soul (JSONL format)
    - Music soul (CSV history format)
    - Consolidation and deduplication
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize soul migrator.
        
        Args:
            verbose: Print migration progress
        """
        self.verbose = verbose
        self.unified_memory = UnifiedMemory(verbose=False)
        
        # Statistics
        self.migrated_language = 0
        self.migrated_music = 0
        self.skipped = 0
        
        if self.verbose:
            print("[Migrator] Initialized")
    
    # =========================================================================
    # LANGUAGE SOUL MIGRATION
    # =========================================================================
    
    def migrate_language_soul(
        self,
        soul_file: str,
        lexicon: Any
    ) -> int:
        """
        Migrate eriamo.soul (Language) to unified memory.
        
        Args:
            soul_file: Path to eriamo.soul (JSONL)
            lexicon: Lexicon instance for keyword extraction
        
        Returns:
            Number of memories migrated
        """
        if not os.path.exists(soul_file):
            if self.verbose:
                print(f"[Migrator] ⚠ Language soul not found: {soul_file}")
            return 0
        
        if self.verbose:
            print(f"\n[Migrator] Loading Language soul: {soul_file}")
        
        migrated = 0
        
        try:
            with open(soul_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    try:
                        data = json.loads(line)
                    except:
                        continue
                    
                    type_tag = data.get('_type', '')
                    
                    # Only migrate @MEMORY and @CORE entries
                    if type_tag not in ['@MEMORY', '@CORE']:
                        continue
                    
                    # Extract data
                    def_id = data.get('id', '')
                    content = data.get('content', '')
                    
                    if not content:
                        self.skipped += 1
                        continue
                    
                    # Extract emotional vector
                    vector_sparse = data.get('vector', {})
                    emotional_state = self._sparse_to_vector(
                        vector_sparse,
                        ['radość', 'smutek', 'strach', 'gniew', 'miłość', 'wstręt', 'zaskoczenie', 'akceptacja']
                    )
                    
                    # Extract keywords from content
                    keywords = self._extract_keywords(content)
                    
                    # Store in unified memory
                    mem_id = self.unified_memory.store_memory(
                        content=content,
                        modalities={
                            'text': {
                                'keywords': keywords,
                                'source': 'language_soul',
                                'original_id': def_id
                            }
                        },
                        emotional_state=emotional_state,
                        ontological_state={},
                        tags=data.get('tags', []),
                        category=data.get('category', 'general'),
                        weight=data.get('weight', 10.0)
                    )
                    
                    migrated += 1
                    
                    if self.verbose and migrated % 100 == 0:
                        print(f"  [Language] {migrated} memories...")
            
            if self.verbose:
                print(f"[Migrator] ✅ Language: {migrated} memories migrated")
            
            self.migrated_language = migrated
            return migrated
            
        except Exception as e:
            if self.verbose:
                print(f"[Migrator] ❌ Language migration error: {e}")
            return migrated
    
    # =========================================================================
    # MUSIC SOUL MIGRATION
    # =========================================================================
    
    def migrate_music_soul(
        self,
        soul_file: str
    ) -> int:
        """
        Migrate music soul files to unified memory.
        
        Args:
            soul_file: Path to soul_history.csv or similar
        
        Returns:
            Number of memories migrated
        """
        if not os.path.exists(soul_file):
            if self.verbose:
                print(f"[Migrator] ⚠ Music soul not found: {soul_file}")
            return 0
        
        if self.verbose:
            print(f"\n[Migrator] Loading Music soul: {soul_file}")
        
        migrated = 0
        
        try:
            import pandas as pd
            
            df = pd.read_csv(soul_file)
            
            # Process unique compositions (filter by description)
            unique_events = df.drop_duplicates(subset=['description'])
            
            for idx, row in unique_events.iterrows():
                description = row.get('description', '')
                
                if not description or pd.isna(description):
                    self.skipped += 1
                    continue
                
                # Extract ontological state
                axes = ['logika', 'emocje', 'affections', 'wiedza', 'czas', 'kreacja', 'byt', 'przestrzen', 'etyka']
                ontological_state = {}
                
                for axis in axes:
                    col_name = f'S_{axis}'
                    if col_name in row:
                        ontological_state[axis] = float(row[col_name])
                
                # Extract emotional message
                emotion_msg = row.get('emotion_msg', '')
                
                # Store in unified memory
                mem_id = self.unified_memory.store_memory(
                    content=description,
                    modalities={
                        'music': {
                            'source': 'music_soul',
                            'event_id': row.get('id_event', idx),
                            'emotion_msg': emotion_msg
                        }
                    },
                    emotional_state=np.zeros(8),  # No language emotions
                    ontological_state=ontological_state,
                    tags=['music', 'composition'],
                    category='music_event',
                    weight=10.0
                )
                
                migrated += 1
                
                if self.verbose and migrated % 50 == 0:
                    print(f"  [Music] {migrated} memories...")
            
            if self.verbose:
                print(f"[Migrator] ✅ Music: {migrated} memories migrated")
            
            self.migrated_music = migrated
            return migrated
            
        except Exception as e:
            if self.verbose:
                print(f"[Migrator] ❌ Music migration error: {e}")
            return migrated
    
    # =========================================================================
    # FULL MIGRATION
    # =========================================================================
    
    def run_full_migration(
        self,
        language_soul: str,
        music_soul: str,
        output_file: str,
        lexicon: Any
    ) -> UnifiedMemory:
        """
        Run complete migration of both souls.
        
        Args:
            language_soul: Path to eriamo.soul
            music_soul: Path to soul_history.csv
            output_file: Path for unified soul output
            lexicon: Lexicon instance
        
        Returns:
            UnifiedMemory instance with migrated data
        """
        if self.verbose:
            print("\n" + "="*70)
            print("  🔄 Soul Migration - Language + Music → Union")
            print("="*70 + "\n")
        
        # Migrate Language
        lang_count = self.migrate_language_soul(language_soul, lexicon)
        
        # Migrate Music
        music_count = self.migrate_music_soul(music_soul)
        
        # Save unified soul
        if self.verbose:
            print(f"\n[Migrator] Saving unified soul to {output_file}")
        
        self.unified_memory.save_to_file(output_file)
        
        # Summary
        if self.verbose:
            print("\n" + "="*70)
            print("  ✅ Migration Complete!")
            print("="*70)
            print(f"  Language: {lang_count} memories")
            print(f"  Music: {music_count} memories")
            print(f"  Total: {self.unified_memory.total_memories}")
            print(f"  Hybrid: {self.unified_memory.hybrid_memories}")
            print(f"  Skipped: {self.skipped}")
            print(f"  Output: {output_file}")
            print("="*70 + "\n")
        
        return self.unified_memory
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def _sparse_to_vector(self, sparse_dict: Dict[str, float], axes: list) -> np.ndarray:
        """Convert sparse dict to numpy vector."""
        vec = np.zeros(len(axes))
        for i, axis in enumerate(axes):
            vec[i] = sparse_dict.get(axis, 0.0)
        return vec
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> list:
        """Extract keywords from text (simple word extraction)."""
        words = text.lower().split()
        
        # Filter out short words and common words
        stopwords = {'i', 'w', 'z', 'na', 'do', 'o', 'się', 'że', 'to', 'jak', 'jest', 'a', 'ale'}
        keywords = [
            w for w in words
            if len(w) > 3 and w not in stopwords
        ]
        
        # Return unique keywords (up to max)
        return list(dict.fromkeys(keywords))[:max_keywords]
    
    def get_migration_report(self) -> Dict[str, Any]:
        """Get migration statistics."""
        return {
            'migrated_language': self.migrated_language,
            'migrated_music': self.migrated_music,
            'total_migrated': self.migrated_language + self.migrated_music,
            'skipped': self.skipped,
            'hybrid': self.unified_memory.hybrid_memories,
            'memory_stats': self.unified_memory.get_statistics()
        }


# =============================================================================
# TEST FUNCTION
# =============================================================================

def test_soul_migrator():
    """Test soul migrator with mock data."""
    print("\n🧪 Testing SoulMigrator\n")
    
    # Create mock Language soul
    print("[Test] Creating mock Language soul...")
    mock_lang_soul = "test_language.soul"
    
    with open(mock_lang_soul, 'w', encoding='utf-8') as f:
        # Meta
        f.write(json.dumps({'_type': '@META', 'version': '2.1'}) + '\n')
        
        # Memories
        for i in range(5):
            mem = {
                '_type': '@MEMORY',
                'id': f'Def_{i:03d}',
                'content': f'Test memory {i}',
                'vector': {'radość': 0.5, 'smutek': 0.2},
                'tags': ['test'],
                'category': 'test',
                'weight': 10.0
            }
            f.write(json.dumps(mem) + '\n')
    
    print("  ✅ Mock Language soul created\n")
    
    # Create mock Music soul
    print("[Test] Creating mock Music soul...")
    mock_music_soul = "test_music.csv"
    
    import pandas as pd
    df = pd.DataFrame({
        'id_event': [1, 2, 3],
        'description': ['Composition 1', 'Composition 2', 'Composition 3'],
        'emotion_msg': ['Happy', 'Sad', 'Calm'],
        'S_logika': [0.5, 0.3, 0.6],
        'S_emocje': [0.8, 0.7, 0.4],
        'S_affections': [0.2, 0.9, 0.3],
        'S_wiedza': [0.4, 0.5, 0.6],
        'S_czas': [0.0, 0.0, 0.0],
        'S_kreacja': [0.7, 0.6, 0.5],
        'S_byt': [0.5, 0.5, 0.5],
        'S_przestrzen': [0.3, 0.2, 0.4],
        'S_etyka': [0.8, 0.8, 0.8]
    })
    df.to_csv(mock_music_soul, index=False)
    
    print("  ✅ Mock Music soul created\n")
    
    # Run migration
    print("[Test] Running migration...")
    migrator = SoulMigrator(verbose=True)
    
    class MockLexicon:
        def analyze_text(self, text, **kwargs):
            return np.zeros(8), None, []
    
    unified = migrator.run_full_migration(
        language_soul=mock_lang_soul,
        music_soul=mock_music_soul,
        output_file='test_unified.soul',
        lexicon=MockLexicon()
    )
    
    # Verify
    assert unified.total_memories == 8, f"Should have 8 memories, got {unified.total_memories}"
    assert unified.text_memories == 5, "Should have 5 text memories"
    assert unified.music_memories == 3, "Should have 3 music memories"
    
    print("\n[Test] Verification...")
    print(f"  Total memories: {unified.total_memories}")
    print(f"  Text: {unified.text_memories}")
    print(f"  Music: {unified.music_memories}")
    print("  ✅ Counts correct\n")
    
    # Cleanup
    for f in [mock_lang_soul, mock_music_soul, 'test_unified.soul']:
        if os.path.exists(f):
            os.remove(f)
    
    print("✅ All SoulMigrator tests passed!\n")


if __name__ == "__main__":
    test_soul_migrator()
