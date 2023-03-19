import torch
import transformers


def load_model(path: str, eight_bit: bool = False, device_map="auto"):
    global model, tokenizer, generator

    if device_map == "zero":
        device_map = "balanced_low_0"

    # config
    gpu_count = torch.cuda.device_count()
    print('gpu_count', gpu_count)

    tokenizer = transformers.LLaMATokenizer.from_pretrained(path)
    model = transformers.LLaMAForCausalLM.from_pretrained(
        path,
        device_map=device_map,
        torch_dtype=torch.float16,
        # max_memory = {0: "14GB", 1: "14GB", 2: "14GB", 3: "14GB",4: "14GB",5: "14GB",6: "14GB", 7: "14GB"},
        load_in_8bit=eight_bit,
        low_cpu_mem_usage=True,
        cache_dir="cache"
    )

    return model.generate, tokenizer


def chat_with_alpaca(model_generator, tokenizer):

    history = []

    with torch.no_grad():

        while True:

            user_input = input("Human: ")

            history.append("Human: " + user_input)

            model_input = "\n\n".join(history) + "\n\nAssistant: "

            gen_in = tokenizer(model_input, return_tensors="pt").input_ids.cuda()

            generated_ids = model_generator(
                gen_in,
                max_new_tokens=200,
                use_cache=True,
                pad_token_id=tokenizer.eos_token_id,
                num_return_sequences=1,
                do_sample=True,
                repetition_penalty=1.1, # 1.0 means 'off'. unfortunately if we penalize it it will not output Sphynx:
                temperature=0.5,        # default: 1.0
                top_k = 50,             # default: 50
                top_p = 1.0,            # default: 1.0
                early_stopping=True,
            )

            generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

            response = generated_text[len(model_input):]

            response = "Assistant:" + response.split(user_input)[0].strip()

            print("\n", response, end="\n\n")

            history.append(response)


if __name__ == "__main__":
    model_generator, tokenizer = load_model(path="./result")

    chat_with_alpaca(model_generator, tokenizer)
