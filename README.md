# point-alpaca

<img src="https://point-alpaca.fra1.cdn.digitaloceanspaces.com/alpaca.png" height="200" width="200">

## What is this?

This is released weights recreated from [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca), an experiment in fine-tuning LLaMA on a synthetic instruction dataset.

## Can I try this somewhere?

Yes! Announcement thread to our frontend where you can try the 7B: https://twitter.com/PointNetwork/status/1637178814210908160

Try it here: https://alpaca.point.space

## How to distill the weights

1. Put LLaMA weights into `original/` folder, such that 7B version would be at `original/7B`

2. Download point-alpaca diffs into `encrypted/` folder:

```
wget -P encrypted/ -i filelist.txt
```

3. Run the following command to decrypt:

```
for f in "encrypted"/*; do if [ -f "$f" ]; then python3 decrypt.py "$f" "original/7B/consolidated.00.pth" "result/"; fi; done
```

Windows users can use the equivalent powershell command: 

```
Get-ChildItem "encrypted" | ForEach-Object {
    if($_.Attributes -eq 'Archive') {
        python3 decrypt.py $_.FullName "original/7B/consolidated.00.pth" "result/"
    }
}
```

You will have finetuned weights in the `result/` folder.

Now that you have them, you can delete the files in `encrypted/` folder.

## How to chat with the model

Other people will probably build better UIs, but for now, try running `python3 chat.py`

But before that, install requirements via `pip3 install -r requirements.txt` (We really recommend installing it in a separate environment, for example, via `conda`)

## Questions? Suggestions?

Find us in our Telegram chat: https://t.me/pointnetworkchat

## Why are weights "encrypted"?

We are not allowed to publish weights for LLaMA, of course, even finetuned, but there is no problem publishing *the difference*, a patch that we suggest to apply to the files. The encryption is a simple XOR between files (not very secure - not recommended for other applications!), ensuring that only the people that have access to the original weights (from completely legal sources, of course) can transform them into finetuned weights.

## What are the checksums so I can check if something is wrong?

```
$ md5sum encrypted/*
4b8622230b59b3f3bcad791c8c1bae51  encrypted/added_tokens.json.75e3ca5df2973756aa612cb17246ef6020a68ff8d94671508987d373642f7a36.enc
876376085d79041818bb7a41bced7819  encrypted/config.json.caf9cac32580e31af8254f66c5a070741d70b15a651721748189180325b7d5a8.enc
44b1feec4c0d1b7c87da24b81c8b8b9e  encrypted/generation_config.json.c5c8961ed243834883fb4e45e8850d3873d6100fde97817f59d275a90eba269d.enc
d127aabb6ad5375bfa97c6ac529c166d  encrypted/pytorch_model-00001-of-00003.bin.90d2ab95a32aeb9362814d8b86db2af5454baab8ea3aa8230c271d6962abb9db.enc
e4b12501e99cf6a30a244af20f5c20ec  encrypted/pytorch_model-00002-of-00003.bin.f3c10a4f5c8beafc6667d34557b64ba479e4dde6ef10672287857b329b7e3229.enc
d212294c06feeb0f14672b68417dbc9e  encrypted/pytorch_model-00003-of-00003.bin.72bf4c96aa6b0c7b56b0336791960da9c75de324ea1131ea4bfc20fde41115c8.enc
e813854dede95a03e5f5b459c7fb32b2  encrypted/pytorch_model.bin.index.json.07ca8edea996b6c3274395fdb2b6c9108f2ffdd610ae55e35c126c21a9d535b1.enc
62503bbf4e91f2b50bf9834757d555d3  encrypted/special_tokens_map.json.4ad09c72922c015ba04f09eabebe38fb34ecb721ca712922c62038eaf2d0bc61.enc
39ec1b33fbf9a0934a8ae0f9a24c7163  encrypted/tokenizer.model.9e556afd44213b6bd1be2b850ebbbd98f5481437a8021afaf58ee7fb1818d347.enc
2c34a03919b6b2b299ad6f77713d0ba0  encrypted/tokenizer_config.json.a5f5efb2240276709a923b1404e08d93cc896fd1bd31fbe173e1e2789ea210ef.enc
560ecf526666cbd485b81f0f16bb9972  encrypted/trainer_state.json.43964ae247e74f4055fe1cf99a7a16efc3114402a1cd918b3cd9e2ebf2858ca9.enc
fe8b25ba7c8dd66d57ce1d3d60f13abd  encrypted/training_args.bin.02f8c3ba14e3c48c05f76880975d7385c878b0e5a0863e352c82f331150d2bd4.enc
```

```
$ md5sum original/7B/consolidated.00.pth
6efc8dab194ab59e49cd24be5574d85e  original/7B/consolidated.00.pth
```

```
$ md5sum result/*
880c59f7618832454595e9820960c360  result/added_tokens.json
d39ed682be60de38e12c5d1974c45620  result/config.json
5300908d1f82b0bc7a4bc79ea00dad66  result/generation_config.json
5d17f8837f9f15538acd65b7d37add2c  result/pytorch_model-00001-of-00003.bin
834b0748527482d60236bc1ec0c71750  result/pytorch_model-00002-of-00003.bin
03dda8d1057b06632fecf399020353b4  result/pytorch_model-00003-of-00003.bin
82559775d42e04199b5a8be8df974b36  result/pytorch_model.bin.index.json
40df8792c753f0d3f5786829efdd2954  result/special_tokens_map.json
eeec4125e9c7560836b4873b6f8e3025  result/tokenizer.model
f2da7d9c67a3b7d2e60a17c540055b85  result/tokenizer_config.json
883795093c1f18baa9b111880b800bf1  result/trainer_state.json
f07e553d22ebe37908bc996953f1bb11  result/training_args.bin
```

## What about larger models?

13B is coming for sure, larger versions - maybe. Consider supporting us if you want it done faster. :)
