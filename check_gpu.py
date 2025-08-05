import tensorflow as tf
import sys
import os

# Suprime logs menos importantes do TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("--- Diagnóstico de GPU para TensorFlow ---")
print(f"Versão do Python: {sys.version}")
print(f"Versão do TensorFlow: {tf.__version__}")
print("-" * 40)

gpus = tf.config.list_physical_devices('GPU')

if gpus:
    print(f"[SUCESSO] GPU(s) encontrada(s): {len(gpus)}")
    for i, gpu in enumerate(gpus):
        print(f"  GPU #{i}: {gpu.name}")
    # Tenta rodar uma pequena operação na GPU
    try:
        with tf.device(gpus[0].name):
            a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
            b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
            c = tf.matmul(a, b)
        print("\n[SUCESSO] Operação de teste na GPU executada com êxito.")
    except Exception as e:
        print(f"\n[ERRO] Falha ao executar operação de teste na GPU: {e}")
else:
    print("[FALHA] Nenhuma GPU compatível foi encontrada pelo TensorFlow.")
    print("Causas comuns:")
    print("  1. Driver da NVIDIA desatualizado ou corrompido.")
    print("  2. Versão do CUDA/cuDNN incompatível com a versão do TensorFlow.")
    print("  3. Problema na instalação das bibliotecas CUDA via pip.")

print("-" * 40)