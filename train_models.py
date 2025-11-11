import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from torch.utils.data import Dataset
import os
from typing import Dict, List


# ============================
# 🔧 CONFIGURATION
# ============================

DATA_FOLDER = "data"
MODEL_SAVE_PATH = "trained_models"

FILES = {
    "lesson_plan": {
        "train": os.path.join(DATA_FOLDER, "lesson_plan_training.json"),
        "val": os.path.join(DATA_FOLDER, "lesson_plan_validation.json"),
    },
    "quiz": {
        "train": os.path.join(DATA_FOLDER, "quiz_training.json"),
        "val": os.path.join(DATA_FOLDER, "quiz_validation.json"),
    }
}

os.makedirs(MODEL_SAVE_PATH, exist_ok=True)


# ============================
# 🧠 DATASET CLASS
# ============================

class AIEducationDataset(Dataset):
    """Dataset class for tokenizing and loading structured JSON data."""

    def __init__(self, data_path: str, tokenizer, task_type: str, dataset_type: str, max_length: int = 512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.task_type = task_type
        self.samples = []
        self._load_data(data_path, dataset_type)

    def _load_data(self, data_path: str, dataset_type: str):
        print(f"\n📘 Loading {dataset_type.upper()} data for '{self.task_type}' from: {data_path}")
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ ERROR: Cannot load {data_path} — {e}")
            return

        # Automatically detect key
        if "quiz_training_dataset" in data:
            data_list = data["quiz_training_dataset"]["samples"]
        elif "lesson_plan_training_dataset" in data:
            data_list = data["lesson_plan_training_dataset"]["samples"]
        elif "quiz_validation_dataset" in data:
            data_list = data["quiz_validation_dataset"]["samples"]
        elif "lesson_plan_validation_dataset" in data:
            data_list = data["lesson_plan_validation_dataset"]["samples"]
        else:
            print(f"❌ ERROR: No recognizable key found in {data_path}.")
            return

        for i, item in enumerate(data_list):
            input_text = item.get("input", "")
            output_json = item.get("output", "")
            if input_text and output_json:
                formatted_output = json.dumps(output_json)
                self.samples.append({
                    "input": input_text,
                    "output": formatted_output
                })

        print(f"✅ Loaded {len(self.samples)} samples for '{self.task_type}' ({dataset_type}).")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        text = f"Instruction: {sample['input']}\nResponse: {sample['output']}{self.tokenizer.eos_token}"

        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        return {
            "input_ids": encoding.input_ids.squeeze(),
            "attention_mask": encoding.attention_mask.squeeze(),
            "labels": encoding.input_ids.squeeze()
        }


# ============================
# ⚙️ TRAINING FUNCTION
# ============================

def train_specific_model(task_type: str, train_path: str, val_path: str):
    print("\n" + "="*60)
    print(f"🚀 STARTING TRAINING FOR: {task_type.upper()}")
    print("="*60)

    model_name = "microsoft/DialoGPT-small"
    print(f"📦 Loading pretrained model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Load datasets
    train_dataset = AIEducationDataset(train_path, tokenizer, task_type, "training")
    val_dataset = AIEducationDataset(val_path, tokenizer, task_type, "validation")

    if len(train_dataset) == 0 or len(val_dataset) == 0:
        print(f"🛑 Skipping {task_type} — no valid data loaded.")
        return

    # Training arguments
    training_args = TrainingArguments(
        output_dir=os.path.join(MODEL_SAVE_PATH, f"{task_type}_checkpoints"),
        num_train_epochs=15,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=4,
        gradient_accumulation_steps=1,
        learning_rate=2e-5,
        warmup_steps=10,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=5,
        eval_strategy="steps",
        eval_steps=10,
        save_strategy="steps",
        save_steps=20,
        load_best_model_at_end=True,
        save_total_limit=3,
        fp16=torch.cuda.is_available(),
        dataloader_pin_memory=False,
        remove_unused_columns=False
    )

    # Trainer setup
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=5)]
    )

    print("🔥 Training started (optimized for small datasets)...")

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    trainer.train()
    print(f"✅ Training for {task_type} completed!")

    final_path = os.path.join(MODEL_SAVE_PATH, f"final_model_{task_type}")
    trainer.save_model(final_path)
    tokenizer.save_pretrained(final_path)
    print(f"📦 Saved fine-tuned {task_type} model to: {final_path}")


# ============================
# 🧩 MAIN EXECUTION
# ============================

if __name__ == "__main__":
    # Train Lesson Plan Model
    train_specific_model(
        task_type="lesson_plan",
        train_path=FILES["lesson_plan"]["train"],
        val_path=FILES["lesson_plan"]["val"]
    )

    # Train Quiz Model
    train_specific_model(
        task_type="quiz",
        train_path=FILES["quiz"]["train"],
        val_path=FILES["quiz"]["val"]
    )

    print("\n🎉 All models (lesson_plan & quiz) trained successfully!")
