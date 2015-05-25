#!/bin/bash

./learn -n data/train.nbest.new.new | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -t 10000 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -t 2000 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -x 200 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -x 20 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -e 0.05 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -e 0.2 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -a 0.1 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -a 0.03 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -i 10 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out2
./learn -n data/train.nbest.new.new -i 3 | ./rerank -n data/test.nbest.new.new -w - | ./grade >> out
