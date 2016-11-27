THEANO_FLAGS=mode=FAST_RUN,optimizer=fast_compile,nvcc.flags=-D_FORCE_INLINES,device=gpu,floatX=float32 python ~/program/python/gpu.py
