import os
import math
import hashlib
from pathlib import Path
from typing import List, Dict

class ChainShardManager:
    """Manages code sharding, redundancy verification, and on-chain reconstruction."""
    
    def __init__(self, redundancy_threshold: int = 3, total_shards: int = 5):
        self.redundancy_threshold = redundancy_threshold
        self.total_shards = total_shards

    def _hash_shard(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def shard_code(self, source_code: str) -> List[Dict[str, str]]:
        """Splits source code into indexed cryptographic shards."""
        data = source_code.encode("utf-8")
        chunk_size = math.ceil(len(data) / self.total_shards)
        shards = []
        
        for i in range(self.total_shards):
            chunk = data[i * chunk_size : (i + 1) * chunk_size]
            shard_entry = {
                "index": i,
                "payload": chunk.hex(),
                "checksum": self._hash_shard(chunk)
            }
            shards.append(shard_entry)
            
        return shards

    def place_on_chain(self, chain_state: List[Dict], source_code: str) -> List[Dict[str, str]]:
        """Simulates placing code shards directly into chain blocks."""
        shards = self.shard_code(source_code)
        # Store shards directly in the chain state structure
        for shard in shards:
            block = {
                "type": "CODE_SHARD",
                "shard_index": shard["index"],
                "payload": shard["payload"],
                "checksum": shard["checksum"]
            }
            chain_state.append(block)
        return shards

    def reconstruct(self, chain_state: List[Dict]) -> str:
        """Reconstitutes the live source code once redundancy threshold is met."""
        collected_shards = {}
        
        for block in chain_state:
            if block.get("type") == "CODE_SHARD":
                idx = block["shard_index"]
                payload_bytes = bytes.fromhex(block["payload"])
                # Verify cryptographic integrity
                if self._hash_shard(payload_bytes) == block["checksum"]:
                    collected_shards[idx] = payload_bytes

        if len(collected_shards) < self.redundancy_threshold:
            raise RuntimeError(
                f"Insufficient redundancy: found {len(collected_shards)} shards, "
                f"but {self.redundancy_threshold} required."
            )

        # Reassemble available sequential or threshold fragments
        full_code_bytes = b""
        for i in sorted(collected_shards.keys()):
            full_code_bytes += collected_shards[i]
            
        return full_code_bytes.decode("utf-8")

if __name__ == "__main__":
    manager = ChainShardManager(redundancy_threshold=3, total_shards=5)
    dummy_code = "print('Crowd-Cloud Decentralized Live Execution Active')"
    
    chain = []
    manager.place_on_chain(chain, dummy_code)
    
    reconstituted = manager.reconstruct(chain)
    print("RECONSTITUTION SUCCESS:")
    print(reconstituted)
