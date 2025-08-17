from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.config import settings
from ..services.llm.factory import create_llm_client


router = APIRouter()


class CodegenRequest(BaseModel):
    pseudocode: str
    framework: str = "pytorch"
    provider: str | None = None
    api_key: str | None = None


class CodegenResponse(BaseModel):
    code: str


@router.post("/generate", response_model=CodegenResponse)
async def generate_code(req: CodegenRequest) -> CodegenResponse:
    provider = req.provider or settings.llm_provider
    api_key = req.api_key or settings.gemini_api_key
    if not api_key:
        # fallback to deterministic stub if no key present
        if req.framework.lower() == "pytorch":
            code = (
                "import torch\n"
                "from torch import nn, optim\n\n"
                "class Model(nn.Module):\n"
                "\tdef __init__(self):\n"
                "\t\tsuper().__init__()\n"
                "\t\tself.net = nn.Sequential(nn.Linear(10, 64), nn.ReLU(), nn.Linear(64, 2))\n\n"
                "\tdef forward(self, x):\n"
                "\t\treturn self.net(x)\n\n"
                "def train_step(model, optimizer, criterion, x, y):\n"
                "\toptimizer.zero_grad()\n"
                "\tpred = model(x)\n"
                "\tloss = criterion(pred, y)\n"
                "\tloss.backward()\n"
                "\toptimizer.step()\n"
                "\treturn loss.item()\n\n"
                "def main():\n"
                "\tmodel = Model()\n"
                "\toptimizer = optim.Adam(model.parameters(), lr=1e-3)\n"
                "\tcriterion = nn.CrossEntropyLoss()\n"
                "\tx = torch.randn(32, 10)\n"
                "\ty = torch.randint(0, 2, (32,))\n"
                "\tfor _ in range(5):\n"
                "\t\tl = train_step(model, optimizer, criterion, x, y)\n"
                "\t\tprint({'loss': l})\n\n"
                "if __name__ == '__main__':\n"
                "\tmain()\n"
            )
        else:
            code = (
                "import tensorflow as tf\n\n"
                "model = tf.keras.Sequential([\n"
                "\ttf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),\n"
                "\ttf.keras.layers.Dense(2)\n"
                "])\n"
                "model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))\n"
                "x = tf.random.normal((32, 10))\n"
                "y = tf.random.uniform((32,), maxval=2, dtype=tf.int32)\n"
                "model.fit(x, y, epochs=3)\n"
            )
        return CodegenResponse(code=code)

    client = create_llm_client(provider, gemini_api_key=api_key)
    system = (
        "You are an expert ML engineer. Convert pseudocode into runnable, self-contained Python code.\n"
        "Target framework: {framework}. Include imports and a minimal train/eval loop if applicable."
    ).format(framework=req.framework)
    text = client.generate_text(
        prompt=f"Pseudocode:\n{req.pseudocode}\n\nReturn only code.",
        system_prompt=system,
        temperature=0.1,
        max_tokens=2048,
    )
    return CodegenResponse(code=text)



