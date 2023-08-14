# cython: language_level=3, c_string_type=str, c_string_encoding=utf8

from _ipyeos cimport *

cdef extern from "_ipyeos.hpp":

    ctypedef struct transaction_trace_proxy:
        uint32_t get_block_num()
        bool is_onblock()

    ctypedef struct ipyeos_proxy:
        transaction_trace_proxy *transaction_trace_proxy_new(void *_transaction_trace_ptr)
        bool transaction_trace_proxy_free(void *transaction_trace_proxy_ptr)

    ipyeos_proxy *get_ipyeos_proxy() nogil

cdef transaction_trace_proxy *proxy(uint64_t ptr):
    return <transaction_trace_proxy*>ptr

def new(uint64_t transaction_trace_proxy_ptr):
    cdef ipyeos_proxy *_proxy = get_ipyeos_proxy()
    return <uint64_t>_proxy.transaction_trace_proxy_new(<void *>transaction_trace_proxy_ptr)

def free(uint64_t ptr):
    cdef ipyeos_proxy *_proxy = get_ipyeos_proxy()
    return _proxy.transaction_trace_proxy_free(<void*>ptr)

def get_block_num(uint64_t ptr):
    return proxy(ptr).get_block_num()

def is_onblock(uint64_t ptr):
    return proxy(ptr).is_onblock()

