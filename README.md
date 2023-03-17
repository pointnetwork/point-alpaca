# point-alpaca

![alpaca](https://point-alpaca.fra1.cdn.digitaloceanspaces.com/alpaca.png){: width=200px}

## What is this?

This is released weights recreated from [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca), an experiment in fine-tuning LLaMA on a synthetic instruction dataset.

## How to distill the weights

1. Put LLaMA weights into `original/` folder, such that 7B version would be at `original/7B`

2. Download point-alpaca diffs into `encrypted/` folder:

```
curl -O -J -L -K filelist.txt -o "encrypted/#1"
```

3. Run the following command to decrypt:

```
for f in "encrypted"/*; do if [ -f "$f" ]; then python3 decrypt.py "$f" "original/7B/consolidated.00.pth" "result/"; fi; done
```

You will have finetuned weights in the `result/` folder.

## How to chat with the model

Other people will probably build better UIs, but for now, try running `python3 chat.py`

But before that, install requirements via `pip3 install -r requirements.txt` (We really recommend installing it in a separate environment, for example, via `conda`)

## Questions? Suggestions?

Find us in our Telegram chat: https://t.me/pointnetworkchat

## Why are weights "encrypted"?

We are not allowed to publish weights for LLaMA, of course, even finetuned, but there is no problem publishing *the difference*, a patch that we suggest to apply to the files. The encryption is a simple XOR between files (not very secure - not recommended for other applications!), ensuring that only the people that have access to the original weights (from completely legal sources, of course) can transform them into finetuned weights.

## What about larger models?

13B is coming for sure, larger versions - maybe. Consider supporting us if you want it done faster. :)