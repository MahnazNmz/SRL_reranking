#!/bin/bash

./learn -n data/train.nbest.new | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -t 10000 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -t 2000 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -x 200 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -x 20 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -e 0.05 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -e 0.2 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -a 0.1 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -a 0.03 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -i 10 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
./learn -n data/train.nbest.new -i 3 | ./rerank -n data/test.nbest.new -w - | ./grade >> out
