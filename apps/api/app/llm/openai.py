"""OpenAI 适配器（与 DeepSeek 实现几乎一致，复用逻辑）."""

from app.llm.deepseek import DeepSeekAdapter


class OpenAIAdapter(DeepSeekAdapter):
    """OpenAI GPT 适配器.

    DeepSeekAdapter 用 OpenAI 兼容协议，OpenAI Adapter 完全相同，
    只是默认 base_url 不同.
    """

    engine = "openai"

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
    ):
        # 不调 super().__init__，直接初始化 OpenAI client
        from openai import AsyncOpenAI

        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )