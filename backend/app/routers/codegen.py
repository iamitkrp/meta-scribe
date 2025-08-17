from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class CodegenRequest(BaseModel):
    pseudocode: str
    framework: str = "pytorch"


class CodegenResponse(BaseModel):
    code: str


@router.post("/generate", response_model=CodegenResponse)
async def generate_code(req: CodegenRequest) -> CodegenResponse:
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



