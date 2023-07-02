# cython: language_level=3, c_string_type=str, c_string_encoding=utf8

from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.map cimport map
from libcpp cimport bool
from libc.stdlib cimport malloc
from libc.stdlib cimport free
from cpython.bytes cimport PyBytes_AsStringAndSize, PyBytes_FromStringAndSize

cdef extern from * :
    ctypedef long long int64_t
    ctypedef unsigned long long uint64_t
    ctypedef int int32_t
    ctypedef unsigned int uint32_t
    ctypedef unsigned short uint16_t
    ctypedef unsigned char uint8_t

cdef extern from "_ipyeos.hpp":
    ctypedef struct eos_cb:
        trace_api_proxy *new_trace_api_proxy(void *chain, string& trace_dir, uint32_t slice_stride, int32_t minimum_irreversible_history_blocks, int32_t minimum_uncompressed_irreversible_history_blocks, uint32_t compression_seek_point_stride)

    ctypedef struct trace_api_proxy:
        bool get_block_trace(uint32_t block_num, string& result)

    ctypedef struct ipyeos_proxy:
        void *new_database_proxy()
        eos_cb *cb

    ipyeos_proxy *get_ipyeos_proxy() nogil

cdef trace_api_proxy *proxy(uint64_t ptr):
    return <trace_api_proxy *>ptr

def new_trace_api(uint64_t chain_ptr, string& trace_dir, uint32_t slice_stride, int32_t minimum_irreversible_history_blocks, int32_t minimum_uncompressed_irreversible_history_blocks, uint32_t compression_seek_point_stride):
    return <uint64_t>get_ipyeos_proxy().cb.new_trace_api_proxy(<void *>chain_ptr, trace_dir, slice_stride, minimum_irreversible_history_blocks, minimum_uncompressed_irreversible_history_blocks, compression_seek_point_stride)

def get_block_trace(uint64_t ptr, uint32_t block_num):
    cdef string result
    cdef bool ret
    ret = proxy(ptr).get_block_trace(block_num, result)
    if ret:
        return result
    else:
        return None
