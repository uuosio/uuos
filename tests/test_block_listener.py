import os
import asyncio
import secrets
import json
import time

from ipyeos import log
from ipyeos.chaintester import ChainTester
from ipyeos.block_state import BlockState
from ipyeos.transaction_trace import TransactionTrace
from ipyeos.packed_transaction import PackedTransaction

logger = log.get_logger(__name__)

def on_accepted_block(block_state_ptr):
    # print("on_accepted_block", block_state_ptr)
    bs = BlockState(block_state_ptr)
    print("block_num", bs.block_num())
    bs.free()

def on_irreversible_block(block_state_ptr):
    # print("on_accepted_block", block_state_ptr)
    bs = BlockState(block_state_ptr)
    block = bs.block()
    print("on irreversible block block_num", bs.block_num(), block.block_num())
    bs.free()

def test_on_accepted_block():
    t = ChainTester()
    t.chain.set_accepted_block_callback(on_accepted_block)
    t.chain.set_irreversible_block_callback(on_irreversible_block)

    for i in range(20):
        t.produce_block()

    logger.info(t.chain.head_block_num())

def on_applied_transaction_event(trace_ptr, signed_tx_ptr):
    logger.info(trace_ptr)
    t = TransactionTrace(trace_ptr)
    logger.info("%s %s %s", t.block_num(), t.is_onblock(), t.get_action_traces_size())
    if t.get_action_traces_size() > 0:
        trace = t.get_action_trace(0)
        logger.info(trace.act())
    
    pt = PackedTransaction(signed_tx_ptr)
    logger.info(pt)
    st = pt.get_signed_transaction()
    logger.info(st.id())

def test_on_applied_transaction_event():
    t = ChainTester()
    t.chain.set_applied_transaction_event_callback(on_applied_transaction_event)
    t.produce_block()
    t.push_action('hello', 'sayhello', b'hello', {'hello':'active'})
    t.produce_block()
