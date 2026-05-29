from __future__ import annotations

from functools import lru_cache

from app.config.settings import Settings, get_settings


class LocalHuggingFaceLLM:
    """Small CPU-oriented Hugging Face generation wrapper."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            self._pipeline = self._build_pipeline()
        return self._pipeline

    def _build_pipeline(self):
        import torch
        from transformers import AutoConfig, AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

        config = AutoConfig.from_pretrained(self.settings.llm_model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.settings.llm_model_name)
        if getattr(config, "is_encoder_decoder", False):
            model = AutoModelForSeq2SeqLM.from_pretrained(
                self.settings.llm_model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(
                self.settings.llm_model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
            )

        return pipeline(
            task="text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1,
        )

    def generate(self, prompt: str) -> str:
        outputs = self.pipeline(
            prompt,
            max_new_tokens=self.settings.llm_max_new_tokens,
            do_sample=False,
            temperature=self.settings.llm_temperature,
            top_p=self.settings.llm_top_p,
            truncation=True,
            return_full_text=False,
        )
        if not outputs:
            return ""
        generated = outputs[0].get("generated_text") or outputs[0].get("summary_text") or ""
        
        # Fallback: if the model still repeats the prompt, strip it manually
        if generated.startswith(prompt):
            generated = generated[len(prompt):]
            
        return generated.strip()


@lru_cache(maxsize=1)
def get_llm() -> LocalHuggingFaceLLM:
    return LocalHuggingFaceLLM()