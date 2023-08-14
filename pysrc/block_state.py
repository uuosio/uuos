from .native_modules import _block_state
from .signed_block import SignedBlock

class BlockState:
    def __init__(self, block_state_proxy_ptr):
        self._ptr = _block_state.new(block_state_proxy_ptr)
    
    def free(self):
        if not self._ptr:
            return
        _block_state.free_block_state(self._ptr)
        self._ptr = None

    def __del__(self):
        self.free()

    def block_num(self):
        return _block_state.block_num(self._ptr)

    def block(self):
        signed_block_ptr = _block_state.block(self._ptr)
        return SignedBlock(signed_block_ptr)
