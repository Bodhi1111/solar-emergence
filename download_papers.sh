#!/bin/bash

echo "📄 SOLAR EMERGENCE - Research Paper Downloader"
echo "=============================================="

# Ensure papers directories exist
mkdir -p knowledge-corpus/raw-inputs/papers/{ai-ml,multimodal,neural-nets,emergent,graph-theory}

echo "📚 Downloading Core AI/ML Papers..."

# Foundational AI Papers
curl -L "https://arxiv.org/pdf/1706.03762.pdf" -o "knowledge-corpus/raw-inputs/papers/ai-ml/attention-is-all-you-need.pdf"
echo "✅ Downloaded: Attention Is All You Need"

curl -L "https://arxiv.org/pdf/1712.01815.pdf" -o "knowledge-corpus/raw-inputs/papers/ai-ml/alphago-zero.pdf"
echo "✅ Downloaded: AlphaGo Zero"

curl -L "https://arxiv.org/pdf/2005.14165.pdf" -o "knowledge-corpus/raw-inputs/papers/ai-ml/gpt3.pdf"
echo "✅ Downloaded: GPT-3"

curl -L "https://arxiv.org/pdf/2203.02155.pdf" -o "knowledge-corpus/raw-inputs/papers/ai-ml/training-language-models.pdf"
echo "✅ Downloaded: Training Language Models"

# Emergent Intelligence Papers
echo "🧠 Downloading Emergent Intelligence Papers..."

curl -L "https://arxiv.org/pdf/1909.07528.pdf" -o "knowledge-corpus/raw-inputs/papers/emergent/emergent-tool-use.pdf"
echo "✅ Downloaded: Emergent Tool Use"

curl -L "https://arxiv.org/pdf/2206.07682.pdf" -o "knowledge-corpus/raw-inputs/papers/emergent/emergent-abilities-llms.pdf"
echo "✅ Downloaded: Emergent Abilities in LLMs"

curl -L "https://arxiv.org/pdf/1803.08375.pdf" -o "knowledge-corpus/raw-inputs/papers/emergent/world-models.pdf"
echo "✅ Downloaded: World Models"

# Multimodal Papers
echo "🎥 Downloading Multimodal Papers..."

curl -L "https://arxiv.org/pdf/2103.00020.pdf" -o "knowledge-corpus/raw-inputs/papers/multimodal/clip.pdf"
echo "✅ Downloaded: CLIP"

curl -L "https://arxiv.org/pdf/2205.06175.pdf" -o "knowledge-corpus/raw-inputs/papers/multimodal/flamingo.pdf"
echo "✅ Downloaded: Flamingo"

curl -L "https://arxiv.org/pdf/1904.01766.pdf" -o "knowledge-corpus/raw-inputs/papers/multimodal/videobert.pdf"
echo "✅ Downloaded: VideoBERT"

curl -L "https://arxiv.org/pdf/2306.05424.pdf" -o "knowledge-corpus/raw-inputs/papers/multimodal/video-chatgpt.pdf"
echo "✅ Downloaded: Video-ChatGPT"

curl -L "https://arxiv.org/pdf/1608.00859.pdf" -o "knowledge-corpus/raw-inputs/papers/multimodal/temporal-segment-networks.pdf"
echo "✅ Downloaded: Temporal Segment Networks"

# Graph Neural Networks & Discovery
echo "🕸️ Downloading GNN & Discovery Papers..."

curl -L "https://arxiv.org/pdf/1812.08434.pdf" -o "knowledge-corpus/raw-inputs/papers/graph-theory/gnn-survey.pdf"
echo "✅ Downloaded: GNN Survey"

curl -L "https://arxiv.org/pdf/1710.04019.pdf" -o "knowledge-corpus/raw-inputs/papers/graph-theory/topological-data-analysis.pdf"
echo "✅ Downloaded: Topological Data Analysis"

curl -L "https://arxiv.org/pdf/1802.03426.pdf" -o "knowledge-corpus/raw-inputs/papers/graph-theory/umap.pdf"
echo "✅ Downloaded: UMAP"

curl -L "https://arxiv.org/pdf/2006.08218.pdf" -o "knowledge-corpus/raw-inputs/papers/neural-nets/self-supervised-learning.pdf"
echo "✅ Downloaded: Self-Supervised Learning"

# Meta-Learning Papers
echo "🎯 Downloading Meta-Learning Papers..."

curl -L "https://arxiv.org/pdf/2004.05439.pdf" -o "knowledge-corpus/raw-inputs/papers/ai-ml/meta-learning-survey.pdf"
echo "✅ Downloaded: Meta-Learning Survey"

curl -L "https://arxiv.org/pdf/1703.03400.pdf" -o "knowledge-corpus/raw-inputs/papers/ai-ml/model-agnostic-meta-learning.pdf"
echo "✅ Downloaded: Model-Agnostic Meta-Learning"

curl -L "https://arxiv.org/pdf/1606.04080.pdf" -o "knowledge-corpus/raw-inputs/papers/ai-ml/one-shot-learning.pdf"
echo "✅ Downloaded: One-Shot Learning"

echo ""
echo "📊 Download Summary:"
echo "Papers downloaded: $(find knowledge-corpus/raw-inputs/papers -name '*.pdf' | wc -l)"
echo ""
echo "✅ All research papers downloaded successfully!"
