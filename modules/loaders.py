import functools

import gradio as gr

from modules import shared

loaders_and_params = {
    'AutoGPTQ': [
        'triton',
        'no_inject_fused_attention',
        'no_inject_fused_mlp',
        'wbits',
        'groupsize',
        'desc_act',
        'gpu_memory',
        'cpu_memory',
        'cpu',
        'disk',
        'auto_devices',
        'trust_remote_code',
    ],
    'GPTQ-for-LLaMa': [
        'gptq_for_llama',
        'wbits',
        'groupsize',
        'model_type',
        'pre_layer',
    ],
    'llama.cpp': [
        'n_ctx',
        'n_gpu_layers',
        'n_batch',
        'threads',
        'no_mmap',
        'mlock',
        'llama_cpp_seed',
    ],
    'Transformers': [
        'cpu_memory',
        'gpu_memory',
        'trust_remote_code',
        'load_in_8bit',
        'bf16',
        'cpu',
        'disk',
        'auto_devices',
        'load_in_4bit',
        'use_double_quant',
        'quant_type',
        'compute_dtype',
        'trust_remote_code',
    ],
}


def get_gpu_memory_keys():
    return [k for k in shared.gradio if k.startswith('gpu_memory')]


@functools.cache
def get_all_params():
    all_params = set()
    for k in loaders_and_params:
        for el in loaders_and_params[k]:
            all_params.add(el)

    if 'gpu_memory' in all_params:
        all_params.remove('gpu_memory')
        for k in get_gpu_memory_keys():
            all_params.add(k)

    return list(sorted(list(all_params)))


def make_loader_params_visible(loader):
    params = loaders_and_params[loader]
    all_params = get_all_params()

    if 'gpu_memory' in params:
        params.remove('gpu_memory')
        params += get_gpu_memory_keys()

    return [gr.update(visible=True) if k in params else gr.update(visible=False) for k in all_params]