import torch, torchvision, torchvision.ops as ops
print("torch:", torch.__version__)
print("torchvision:", torchvision.__version__)
print("CUDA available:", torch.cuda.is_available())

# Optional: tiny NMS check on GPU
if torch.cuda.is_available():
    import torch as T
    boxes = T.tensor([[0., 0., 10., 10.]], device="cuda")
    scores = T.tensor([0.5], device="cuda")
    ops.nms(boxes, scores, 0.5)
    print("✅ torchvision.ops.nms works on CUDA")